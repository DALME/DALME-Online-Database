from datetime import datetime
from django import forms
from django.core.mail import EmailMessage
from dalme_app.utils import Search


class ContactForm(forms.Form):
    name = forms.CharField(max_length=127, required=True, label='Your Name')
    email = forms.EmailField(required=True, label='Your Email')
    subject = forms.CharField(max_length=127, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def save(self):
        email = EmailMessage(
            self.cleaned_data['subject'],
            self.cleaned_data['message'],
            f"{self.cleaned_data['name']} <{self.cleaned_data['email']}>",
            ['projectdalme@gmail.com'],
            reply_to=[self.cleaned_data['email']]
        )
        try:
            email.send(fail_silently=False)
            return True, ''
        except Exception as e:
            return False, e


class SourceFilterForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()

        date_range = self.data.get('date_range')
        if date_range:
            try:
                after, before = date_range.split(',')
            except ValueError:
                self.add_error(
                    'date_range', f'Incorrect date format, should be: %Y,%Y'
                )
            after = f'{after}-01-01'
            before = f'{before}-12-31'

            try:
                after, before = [
                    datetime.strptime(value, '%Y-%m-%d')
                    for value in [after, before]
                ]
            except ValueError:
                self.add_error(
                    'date_range',
                    f'Malformed date value for an element of: {date_range}'
                )

            cleaned_data['date_range'] = [after, before]

        return cleaned_data


class SearchForm(forms.Form):

    MATCH_TYPES = (
        ('exact', 'Exact match'),
        ('fuzzy', 'Fuzzy match'),
        ('prefix', 'Prefix match')
    )

    OPERATORS = (
        ('and', 'AND'),
        ('or', 'OR'),
    )

    FIELDS = (
        ('', 'Field'),
        ('name', 'Name'),
        ('text', 'Transcription'),
        ('description', 'Description'),
        ('source_type', 'Record Type'),
        ('locations', 'Location'),
    )

    WILDCARDS = (
        ('', 'Wildcard'),
        ('*', '*'),
        ('?', '?'),
    )

    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={'type': 'search'}),
    )
    match_type = forms.ChoiceField(
        required=False,
        label="Match",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        choices=MATCH_TYPES
    )
    operator = forms.ChoiceField(
        required=False,
        label="Operator",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm form-operator'}),
        choices=OPERATORS
    )
    wildcards = forms.ChoiceField(
        required=False,
        label="Wildcars",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        choices=WILDCARDS
    )
    field = forms.ChoiceField(
        required=False,
        label="Field",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        choices=FIELDS
    )
    field_value = forms.CharField(
        required=False,
        label="Query",
        widget=forms.TextInput(
            attrs={
                'type': 'search',
                'placeholder': 'Query',
                'autocomplete': 'off',
                'autocorrect': 'off',
                'autocapitalize': 'off',
                'spellcheck': 'false',
                'class': 'form-control form-control-sm'
            }
        ),
    )

    def search(self, **kwargs):
        if not self.is_valid():
            return None

        if not self.cleaned_data.get("q"):
            return None

        return Search(self.cleaned_data, **kwargs)
