from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms
from .models import Comment
from captcha.fields import CaptchaField


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('captcha', attrs={'font-size': '16px'}),
        )

    class Meta:
        model = Comment
        fields = ['author', 'email', 'home_page', 'text', 'file']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }