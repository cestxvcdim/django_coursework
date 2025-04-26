from django import forms

from blog.models import Post
from mailing.forms import StyleFormMixin


class PostForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "body", "image")
