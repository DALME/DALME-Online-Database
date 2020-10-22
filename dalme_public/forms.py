from datetime import datetime
from django import forms
from django.core import mail
from haystack.query import EmptySearchQuerySet, SearchQuerySet


class ContactForm(forms.Form):
    name = forms.CharField(max_length=127, required=True, label='Your Name')
    email = forms.EmailField(required=True, label='Your Email')
    subject = forms.CharField(max_length=127, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def get_mail_kwargs(self):
        return {
            'subject': self.cleaned_data['subject'],
            'message': self.cleaned_data['message'],
            'from_email': self.cleaned_data['email'],
            'recipient_list': ['projectdalme@gmail.com'],
            'fail_silently': False,
        }

    def save(self):
        mail.send_mail(**self.get_mail_kwargs())


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
    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"type": "search"}),
    )

    def __init__(self, *args, **kwargs):
        self.searchqueryset = kwargs.pop("searchqueryset", None)
        self.load_all = kwargs.pop("load_all", False)

        if self.searchqueryset is None:
            self.searchqueryset = SearchQuerySet()

        super(SearchForm, self).__init__(*args, **kwargs)

    def no_query_found(self):
        """Determines the behavior when no query was found ->
        no results are returned (``EmptySearchQuerySet``)."""
        return EmptySearchQuerySet()

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get("q"):
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data["q"])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs.highlight()

    def get_suggestion(self):
        if not self.is_valid():
            return None

        return self.searchqueryset.spelling_suggestion(self.cleaned_data["q"])
