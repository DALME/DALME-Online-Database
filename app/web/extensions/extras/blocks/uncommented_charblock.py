"""Uncommented char block."""

from wagtail.blocks import CharBlock

from django import forms
from django.forms import TextInput


class UncommentedTextInput(TextInput):
    show_add_comment_button = False


class UncommentedCharBlock(CharBlock):
    def __init__(  # noqa: PLR0913
        self,
        required=True,
        help_text=None,
        max_length=None,
        min_length=None,
        validators=(),
        search_index=True,
        **kwargs,
    ):
        self.search_index = search_index
        self.field = forms.CharField(
            required=required,
            help_text=help_text,
            max_length=max_length,
            min_length=min_length,
            validators=validators,
            widget=UncommentedTextInput,
        )
        super(CharBlock, self).__init__(**kwargs)
