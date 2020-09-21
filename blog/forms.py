from django import forms

from .models import Post, Category, Tags
from site_settings.forms import BaseForm

from tinymce.widgets import TinyMCE


class CreatePostForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Post
        fields = ['active', 'title', ]


class PostForm(BaseForm, forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Post
        fields = ['active', 'is_featured', 'title', 'category', 'text', 'tags']


class CategoryForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Category
        fields = ['title']


class TagForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Tags
        fields = ['title', ]
