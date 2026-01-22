# Footnotes Extension

## Installation instructions

- Add the extension to `INSTALLED_APPS` in the Django settings file:

```python
INSTALLED_APPS = [
    # ...
    'web.extensions.footnotes',
    # ...
]
```

- Add the extension's urls to your project's `urls.py` file:

```python
from web.extensions.footnotes.urls import urlpatterns as footnote_urls

cmsurls = [
    *biblio_urls,
    *footnote_urls,
    *saved_search_urls,
    path('', include(wagtailadmin_urls)),
]

urlpatterns = [
    # ...
     *footnote_urls,
    # ...
]
```

- Add the `FootnotesPlaceMarker` block to any StreamField where footnotes should be available (or to the default set of blocks):

```python
from web.extensions.footnotes.blocks import get_default_blocks

body = StreamField(get_default_blocks())
```

- Make sure that any page where footnotes are to be used inherits from `FootnoteMixin`:

```python
from web.extensions.footnotes.models import FootnoteMixin

class BasePage(Page, FootnoteMixin):
    # page definitions

```

- Include the `footnotes/footnote_container.html` below the main content in your page tamplates:

```python
    # main page content
    {% if page.has_footnotes and not page.has_placemarker %}
        {% include "footnotes/footnote_container.html" with footnotes=page.footnotes %}
    {% endif %}
```

- Lastly, make and run migrations:

```bash
python manage.py makemigrations
python manage.py migrate

```
