from django import forms
from django.utils.html import escape

from .models import Comment
from captcha.fields import CaptchaField


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    def clean_text(self):
        text = self.cleaned_data['text']
        # Validate and sanitize HTML tags
        text = escape(text)
        return text

    class Meta:
        model = Comment
        fields = ['author', 'email', 'home_page', 'text', 'file']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }