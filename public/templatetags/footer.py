"""Templatetag to return footer."""

from django import template

from public.models import FooterLink, SocialMedia

register = template.Library()


@register.inclusion_tag('public/includes/footer.html', takes_context=True)
def footer(context):
    return {
        'links': FooterLink.objects.all(),
        'social': SocialMedia.objects.all(),
        'page': context['page'],
        'request': context['request'],
    }
