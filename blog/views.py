from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from .models import Post
from .forms import PostForm
from .tables import PostTable


class PostListView(ListView):
    template_name = 'blog/bloglist.html'
    model = Post
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)

        return context


class PostDetailView(DetailView):
    template_name = 'blog/blogDetail.html'
    model = Post
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


# dashboard views


@method_decorator(staff_member_required, name='dispatch')
class DashboardBlogListView(ListView):
    template_name = 'dashboard/list_page.html'
    model = Post

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['qs_table'] = PostTable(self.object_list)

        return context


@method_decorator(staff_member_required, name='dispatch')
class DashboardBlogCreateView(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'dashboard/form.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardBlogCreateView, self).get_context_data(**kwargs)
        context['back_url'] = reverse()
        return context



@method_decorator(staff_member_required, name='dispatch')
class DashboardBlogUpdateVuew(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'dashboard/form.html'


@staff_member_required
def post_delete_view(request, pk):
    instance = get_object_or_404(Post, id=pk)
    instance.delete()
    return redirect(reverse('dashboard_blog:post_list'))