from django.forms import ModelForm

from .models import Post
from site_settings.forms import BaseForm


class PostForm(BaseForm, ModelForm):

    class Meta:
        model = Post
        fields = '__all__'