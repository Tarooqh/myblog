from django import forms
from pagedown.widgets import PagedownWidget
from .models import posts


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = posts
        fields=[
            "title",
            "content",
            "image",
            "draft",
            "publish"
        ]