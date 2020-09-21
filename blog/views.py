from django.shortcuts import render, get_object_or_404, redirect, reverse,HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse

from django_tables2 import RequestConfig
from .models import Post, Category, Tags
from .forms import PostForm, CreatePostForm, CategoryForm, TagForm
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
        queryset_table = PostTable(self.object_list)
        RequestConfig(self.request, paginate={"per_page": self.paginate_by}).configure(queryset_table)
        context['queryset_table'] = PostTable(self.object_list)
        context['create_url'] = reverse('dashboard_blog:post_create')
        context['page_title'] = 'Blog'
        return context


@method_decorator(staff_member_required, name='dispatch')
class DashboardBlogCreateView(CreateView):
    form_class = CreatePostForm
    model = Post
    template_name = 'dashboard/form.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardBlogCreateView, self).get_context_data(**kwargs)
        context['back_url'] = reverse('dashboard_blog:post_list')
        context['page_title'] = 'Δημιουργια νεου Post'
        return context

    def form_valid(self, form):
        obj = form.save()
        return redirect(obj.get_edit_url())


@method_decorator(staff_member_required, name='dispatch')
class DashboardBlogUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/dashboard/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardBlogUpdateView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tags.objects.all()
        context['category_form'] = CategoryForm()
        context['tag_form'] = TagForm()
        return context


@staff_member_required
def post_delete_view(request, pk):
    instance = get_object_or_404(Post, id=pk)
    instance.delete()
    return redirect(reverse('dashboard_blog:post_list'))


@staff_member_required
def ajax_update_category_view(request, pk):
    print('the backend is trigger')
    obj = get_object_or_404(Category, id=pk)
    form = CategoryForm(instance=obj)
    data = {}
    response = render_to_string('blog/dashboard/ajax_modal.html',
                                context={
                                    'form': form,
                                    'form_title': f'Επεξεργασια {obj.title}',
                                    'delete_url': obj.get_delete_url(),
                                    'action_url': obj.get_update_url()
                                })
    data['result'] = response
    return JsonResponse(data)



@staff_member_required
def validate_category_creation_view(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        obj = form.save()
        messages.success(request, f'Η κατηγορια {obj.title} δημιουργηθηκε')
    else:
        messages.warning(request, form.errors)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def validate_category_edit_or_delete_view(request, pk,action):
    obj = get_object_or_404(Category, id=pk)
    if action == 'delete':
        obj.delete()
        messages.warning(request, f'H Κατηγορια {obj.title} διαγράφηκε.')
    elif action == 'update':
        form = CategoryForm(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Η κατηγορισ επεξεργαστηκε επιτυχως')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@staff_member_required
def ajax_update_tag_view(request, pk):
    obj = get_object_or_404(Tags, id=pk)
    form = TagForm(instance=obj)
    data = {}
    data['result'] = render_to_string('blog/dashboard/ajax_modal.html',
                                      context={
                                          'form': form,
                                          'form_title': f'Επεξεργασια {obj.title}',
                                          'action_url': '',
                                          'delete_url': ''
                                      })
    return JsonResponse(data)


@staff_member_required
def validate_update_or_delete_tag_view(request, pk, action):
    obj = get_object_or_404(Tags, id=pk)
    if action == 'delete':
        obj.delete()
    elif action == 'update':
        form = TagForm(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Επεξεργασια {obj}')
        else:
            messages.warning(request, form.errors)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_tag_creation_view(request):
    form = TagForm(request.POST or None)
    if form.is_valid():
        obj = form.save()
        messages.success(request, f'Το tag {obj} δημιουργηθηκε!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
