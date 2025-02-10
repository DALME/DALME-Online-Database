"""Forms for web app."""

from django_recaptcha import fields, widgets

from django import forms
from django.core.mail import EmailMessage

from web.models.settings import Settings


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
            f'{self.cleaned_data["name"]} <{self.cleaned_data["email"]}>',
            [Settings.objects.first().contact_email],
            reply_to=[self.cleaned_data['email']],
        )
        try:
            email.send(fail_silently=False)
        except Exception as e:  # noqa: BLE001
            return False, e

        return True, ''
