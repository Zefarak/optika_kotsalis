import django_tables2 as tables

from .models import Post


class PostTable(tables.Table):
    action = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' class='btn btn-primary btn-round'>"
                                   "<i class='fa fa-edit'> </i></a>",
                                   orderable=False, verbose_name='Επεξεργασια'
                                   )

    class Meta:
        model = Post
        fields = ['timestamp', 'title', 'is_featured', 'active', 'action' ]
        template_name = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table  table-hover'}
