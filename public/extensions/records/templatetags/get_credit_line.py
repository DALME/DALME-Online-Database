"""Templatetag to return record credit line."""

from django import template

register = template.Library()


def get_names_as_string(names):
    return (
        f'{names[0]}'
        if len(names) == 1
        else f'{names[0]} and {names[1]}'
        if len(names) == 2  # noqa: PLR2004
        else f'{", ".join(names[:-1])}, and {names[-1]}'
    )


@register.simple_tag(takes_context=True)
def get_credit_line(context):
    record = context.get('record', False)
    if record:
        editors, corrections, contributors = context['data']['credits']
        if editors:
            cline = f'Edited by {get_names_as_string(editors)}'
        else:
            try:
                cline = f"Edited by the {context.get('request').tenant.project.name} Team"
            except:  # noqa: E722
                cline = 'Edited by the IDA Team'

        cline = cline + f', with corrections by {get_names_as_string(corrections)}' if corrections else cline
        cline = (
            cline + f', and contributions by {get_names_as_string(contributors)}'
            if corrections and contributors
            else cline
        )
        cline = (
            cline + f', with contributions by {get_names_as_string(contributors)}'
            if contributors and not corrections
            else cline
        )
        return cline + '.'
    return ''
