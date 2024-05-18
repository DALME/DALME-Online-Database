"""Templatetag to return footer."""

from django import template

from public.models import FooterLink, Settings, SocialMedia

register = template.Library()


@register.inclusion_tag('public/includes/footer.html', takes_context=True)
def footer(context):
    request = context.get('request')
    try:
        show_login = request.user.is_anonymous
    except AttributeError:
        show_login = True

    return {
        'links': FooterLink.objects.all(),
        'social': SocialMedia.objects.all(),
        'settings': Settings.objects.first(),
        'page': context['page'],
        'request': request,
        'show_login': show_login,
    }
