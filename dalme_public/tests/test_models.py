from unittest import mock

import pytest

from django.core.exceptions import ValidationError

from dalme_public.models import Collection


@mock.patch('dalme_public.models.Collection.alias_type', new_callable=mock.PropertyMock)
def test_set_alias_model_clean_mismatch_error(mock_alias_type):
    mock_alias_type.return_value = 2
    instance = Collection()
    with pytest.raises(ValidationError) as excinfo:
        instance.clean()
    assert 'Collection.set_type mismatch: 1 != 2' in str(excinfo.value)


@mock.patch('dalme_public.models.Collection.alias_type', new_callable=mock.PropertyMock)
def test_set_alias_model_clean_none_passes(mock_alias_type):
    mock_alias_type.return_value = None
    instance = Collection()
    instance.clean()


@mock.patch('dalme_public.models.Collection.alias_type', new_callable=mock.PropertyMock)
def test_set_alias_model_clean_match_passes(mock_alias_type):
    mock_alias_type.return_value = 1
    instance = Collection()
    instance.clean()
