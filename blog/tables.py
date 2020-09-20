import django_tables2 as tables

from .models import Post


class PostTable(tables.Table):

    class Meta:
        model = Post
        fields = ['title']