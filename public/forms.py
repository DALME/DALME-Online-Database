"""Define forms for public."""

from django_recaptcha import fields, widgets

from django import forms
from django.core.mail import EmailMessage

from ida.models import SavedSearch


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=127,
        required=True,
        label='Your Name',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        required=True,
        label='Your Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    subject = forms.CharField(
        max_length=127,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )
    captcha = fields.ReCaptchaField(
        widget=widgets.ReCaptchaV2Checkbox(),
    )

    def save(self):
        email = EmailMessage(
            self.cleaned_data['subject'],
            self.cleaned_data['message'],
            f"{self.cleaned_data['name']} <{self.cleaned_data['email']}>",
            ['projectdalme@gmail.com'],
            reply_to=[self.cleaned_data['email']],
        )
        try:
            email.send(fail_silently=False)
        except Exception as e:  # noqa: BLE001
            return False, e

        return True, ''


class RecordFilterForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()

        date_range = self.data.get('date_range')
        if date_range:
            try:
                after, before = date_range.split(',')
            except ValueError:
                self.add_error(
                    'date_range',
                    'Incorrect date format, should be: YYYY,YYYY',
                )

            cleaned_data['date_range'] = [after, before]

        return cleaned_data


class SavedSearchLinkChooserForm(forms.Form):
    id = forms.ChoiceField(required=True, choices=[], label='Saved search')
    link_text = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        search_list = [(i.id, i.name) for i in SavedSearch.objects.all()]
        super().__init__(*args, **kwargs)
        self.fields['id'].choices = search_list


class BibliographyLinkChooserForm(forms.Form):
    id = forms.CharField(required=True, label='Entry')
    link_text = forms.CharField(required=False)


class FootnoteChooserForm(forms.Form):
    note_id = forms.CharField(widget=forms.HiddenInput())
    text = forms.CharField(widget=forms.Textarea)
