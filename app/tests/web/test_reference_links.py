"""Test the bibliography reference link handler."""

from web.extensions.bibliography.rich_text import ReferenceLinkHandler


def test_a_reference_links_to_the_bibliography_on_the_same_host():
    html = ReferenceLinkHandler.expand_db_attributes({'data-id': 'smith-1998'})

    assert html == '<a href="/project/bibliography/#smith-1998">'
