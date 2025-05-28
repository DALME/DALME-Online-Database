"""Unit tests for the data type definitions."""

import app.abstract.__init__ as abstract_init


def test_base_data_types_content():
    expected = (
        ('BOOL', 'BOOL (boolean)'),
        ('INT', 'INT (integer)'),
        ('JSON', 'JSON (data)'),
        ('STR', 'STR (string)'),
    )
    assert expected == abstract_init.BASE_DATA_TYPES


def test_data_types_sorted_and_content():
    # Should contain all base types plus the extras, sorted by key
    expected_keys = ['BOOL', 'DATE', 'FKEY', 'FLOAT', 'INT', 'JSON', 'RREL', 'STR']
    actual_keys = [item[0] for item in abstract_init.DATA_TYPES]
    assert actual_keys == sorted(expected_keys)
    # Check that all expected types are present
    for key in expected_keys:
        assert any(item[0] == key for item in abstract_init.DATA_TYPES)
