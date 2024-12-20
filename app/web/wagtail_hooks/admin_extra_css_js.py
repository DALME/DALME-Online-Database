"""Add extra css and javascript to admin."""

from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html


def extra_admin_css():
    return format_html(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css" integrity="sha512-1PKOgIY59xJ8Co8+NE6FZ+LOAZKjy+KY8iq0G4B3CyeY6wYHN3yt9PW0XpSriVlkMXe40PTKnXrLnZ9+fkDaog==" crossorigin="anonymous" /> \
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/select2/3.5.4/select2.min.css" integrity="sha512-iVAPZRCMdOOiZWYKdeY78tlHFUKf/PqAJEf/0bfnkxJ8MHQHqNXB/wK2y6RH/LmoQ0avRlGphSn06IMMxSW+xw==" crossorigin="anonymous" referrerpolicy="no-referrer" /> \
        <link rel="stylesheet" href="{}">',
        static('common/css/admin.css'),
    )


def extra_admin_js():
    return format_html(
        '<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/citation-js@0.4.10/build/citation.min.js" integrity="sha256-vqUHuIyFzuc0osFFLRQk5hhFPLGHSnc4jvAtp9lZYvo=" crossorigin="anonymous"></script> \
        <script src="https://cdnjs.cloudflare.com/ajax/libs/select2/3.5.4/select2.min.js" integrity="sha512-jfp1Gv+A3dHho9qOUUWOrZA6NWR08j7GYVn8VXcRI0FsDb3xe0hQHVwasi2UarjZzPYOxT5uvmlHrWLXQ+M4AQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script> \
        <script type="text/javascript">window.cite = require("citation-js")</script>\
        <script type="text/javascript" src="{}"></script>\
        <script type="text/javascript" src="{}"></script>\
        <script type="text/javascript">window.APIURL = "{}"</script>',
        static('common/js/wagtailUtils.js'),
        static('common/js/wagtailAdminStartup.js'),
        settings.API_URL,
    )
