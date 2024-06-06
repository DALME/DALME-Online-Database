"""Helper functions for working with records."""

from ida.context import get_current_tenant


def names_to_string(names):
    """Convert a list of names to a string."""
    return (
        f'{names[0]}'
        if len(names) == 1
        else f'{names[0]} and {names[1]}'
        if len(names) == 2  # noqa: PLR2004
        else f'{", ".join(names[:-1])}, and {names[-1]}'
    )


def format_credits(record):
    """Return formated credits for a record, if applicable."""
    if not record:
        return None

    try:
        c_data = record.get_credit_data()
        editors = [i['name'] for i in c_data if i['credit'] == 'editor']
        corrections = [i['name'] for i in c_data if i['credit'] == 'corrections']
        contributors = [i['name'] for i in c_data if i['credit'] == 'contributor']
    except:  # noqa: E722
        editors, corrections, contributors = [], [], []

    if not editors:
        try:  # noqa: SIM105
            editors = [record.owner.agent.first().standard_name]
        except:  # noqa: E722
            pass
    return (editors, corrections, contributors)


def format_credit_line(record):
    """Return formatted credit line for a record, if applicable."""
    if not record:
        return ''

    editors, corrections, contributors = format_credits(record)
    try:
        project = get_current_tenant().project.name
    except:  # noqa: E722
        project = 'IDA'

    if editors:
        cline = f'Edited by {names_to_string(editors)}'
    else:
        try:
            cline = f'Edited by the {project} Team'
        except:  # noqa: E722
            cline = 'Edited by the IDA Team'

    cline = cline + f', with corrections by {names_to_string(corrections)}' if corrections else cline
    cline = cline + f', and contributions by {names_to_string(contributors)}' if corrections and contributors else cline
    cline = (
        cline + f', with contributions by {names_to_string(contributors)}'
        if contributors and not corrections
        else cline
    )
    return cline + '.'


def get_record_format(record):
    try:
        format_values = {
            i['attribute_type__name']: i['value'].lower()
            for i in record.attributes.filter(
                attribute_type__name__in=['support', 'format'],
            ).values('attribute_type__name', 'value')
        }
        format_values['label'] = ', '.join([format_values.get('support'), format_values.get('format')])
    except:  # noqa: E722
        return None
    else:
        return format_values


def get_archival_location(record):
    try:
        name = record.name
        archive_name = record.parent.name
        loc = name.replace(archive_name, '').strip() if archive_name in name else None
        return loc[1:] if loc and loc.startswith(',') else loc
    except:  # noqa: E722
        return None


def format_source(record):
    """Return formatted source information for a record."""
    parent = record.parent
    if parent.__class__.__name__ == 'RecordGroup':
        url_attr = parent.parent.attributes.filter(attribute_type__name='url')
        return {
            'type': 'register',
            'format': get_record_format(parent),
            'name': parent.parent.name,
            'url': url_attr.first().value if url_attr.exists() else None,
            'loc': get_archival_location(parent),
        }

    zotero_attr = parent.attributes.filter(attribute_type__name='zotero_key')
    return {
        'type': 'edition',
        'name': parent.name,
        'zotero_key': zotero_attr.first().value if zotero_attr.exists() else None,
    }
