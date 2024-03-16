"""Templatetag to return record credit line."""

from django import template

from public.templatetags import get_names_as_string

register = template.Library()


@register.simple_tag(takes_context=True)
def get_credit_line(context):
    record = context.get('record', False)
    if record:
        editors, corrections, contributors = context['data']['get_credits']
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
