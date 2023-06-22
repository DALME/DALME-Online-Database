from django import forms


class SearchForm(forms.Form):
    """Search form for Django-based frontend."""

    JOIN_TYPES = (
        ('must', 'AND'),
        ('must_not', 'NOT'),
        ('should', 'OR'),
    )

    QUERY_TYPES = (
        ('match_phrase', 'the following word(s)'),
        ('match', 'word(s) similar to'),
        ('prefix', 'word(s) beginning with'),
        ('term', 'exactly this expression'),
    )

    RANGE_TYPES = (
        ('value', 'exactly'),
        ('lt', 'before'),
        ('gt', 'after'),
    )

    join_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm form-operator'}),
        choices=JOIN_TYPES,
        help_text='<p class=&quot;text-left p-1&quot;>\
                    <b>AND:</b> both the current and previous clauses must match<br/> \
                    <b>NOT:</b> the current clause must not match<br/> \
                    <b>OR:</b> either the current or previous clauses must match<br/></p>',
    )

    field = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        choices=[],
        help_text='Field to search',
    )

    field_type = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        initial='text',
    )

    query_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        choices=QUERY_TYPES,
        help_text='<p class=&quot;text-left p-1&quot;>\
                    <b>the following word(s):</b> the query, as entered, must be present in the field.<br/>\
                    <b>word(s) similar to:</b> ignores word order and also finds word(s) that vary by 1-2 letters from the query.<br/>\
                    <b>word(s) beginning with:</b> matches words that begin with the characters in the query.<br/>\
                    <b>exactly this expression:</b> the query must exactly match the contents of the field.<br/><p>',
    )

    range_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        choices=RANGE_TYPES,
        help_text='<p class=&quot;text-left p-1&quot;> \
                    <b>Exactly:</b> matches the date in the query<br/> \
                    <b>Before:</b> matches any date before the date in the query<br/> \
                    <b>After with:</b> matches any date after the date in the query<br/></p>',
    )

    field_value = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'search',
                'placeholder': 'Type a query to search in record names',
                'autocomplete': 'off',
                'autocorrect': 'off',
                'autocapitalize': 'off',
                'spellcheck': 'false',
                'class': 'form-control form-control-sm',
            },
        ),
        help_text='Value to search',
    )

    query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'search',
                'placeholder': 'Query',
                'autocomplete': 'off',
                'autocorrect': 'off',
                'autocapitalize': 'off',
                'spellcheck': 'false',
                'class': 'form-control form-control-sm',
            },
        ),
    )

    def __init__(self, *args, **kwargs):  # noqa: D107
        fields = kwargs.pop('fields', [])
        super().__init__(*args, **kwargs)
        self.fields['field'].choices = fields
