from django import forms
from django.core.validators import URLValidator
from django.utils.html import escape

from .models import Comment
from captcha.fields import CaptchaField


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    def clean_text(self):
        text = self.cleaned_data['text']
        # Validate and sanitize HTML tags
        allowed_tags = ['a', 'code', 'i', 'strong']
        text = escape(text)
        return text

    def clean_home_page(self):
        home_page = self.cleaned_data['home_page']
        # Validate URL format for home page
        if home_page:
            validate_url = URLValidator()
            try:
                validate_url(home_page)
            except forms.ValidationError:
                raise forms.ValidationError('Invalid URL format for home page')
        return home_page

    class Meta:
        model = Comment
        fields = ['author', 'email', 'home_page', 'text', 'file']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }