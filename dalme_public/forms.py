from datetime import datetime
from django import forms
from django.core.mail import EmailMessage
from captcha import fields, widgets


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
        widget=widgets.ReCaptchaV2Checkbox()
    )

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
