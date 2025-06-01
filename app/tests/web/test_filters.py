"""Tests for the FeaturedFilter functionality in web.filters."""

import pytest

from web.filters import FeaturedFilter
from web.models import Essay


@pytest.mark.django_db
def test_featured_filter_kind_and_date_grouping(featured_pages, featured_pages_qs):
    # Filter for essays, order by date
    years = list({page.last_published_at.year for page in featured_pages if isinstance(page, Essay)})
    years.sort(reverse=True)
    data = {'kind': 'essay', 'order_by': 'date'}
    filtered = FeaturedFilter(data=data, queryset=featured_pages_qs)
    # Should only include essays, grouped by year and month
    for i, group in enumerate(filtered.qs):
        assert group[0] == years[i]
        for page in group[1]:
            assert isinstance(page, Essay)
            assert page.last_published_at.year == years[i]


@pytest.mark.django_db
def test_featured_filter_order_by_owner(featured_pages, featured_pages_qs):
    essay_owners = [page.owner.last_name for page in featured_pages if isinstance(page, Essay)]
    essay_owners.sort()
    data = {'kind': 'essay', 'order_by': 'owner'}
    filtered = FeaturedFilter(data=data, queryset=featured_pages_qs)
    for i, group in enumerate(filtered.qs):
        for page in group:
            assert page.owner.last_name == essay_owners[i]


@pytest.mark.django_db
def test_featured_filter_no_kind(featured_pages, featured_pages_qs):
    years = list({page.last_published_at.year for page in featured_pages})
    years.sort(reverse=True)
    data = {'order_by': 'date'}
    filtered = FeaturedFilter(data=data, queryset=featured_pages_qs)
    for i, group in enumerate(filtered.qs):
        assert group[0] == years[i]


@pytest.mark.django_db
def test_featured_filter_empty_queryset():
    data = {'kind': 'essay', 'order_by': 'date'}
    f = FeaturedFilter(data=data, queryset=Essay.objects.none())
    grouped = f.qs
    assert grouped == []
