from django.urls import path

from .views import DashboardBlogListView, DashboardBlogCreateView, DashboardBlogUpdateVuew, post_delete_view

app_name = 'dashboard_blog'

urlpatterns = [
    path('list/', DashboardBlogListView.as_view(), name='post_list'),
    path('detail/<slug:slug>/', DashboardBlogUpdateVuew.as_view(), name='post_detail'),
    path('delete/<int:pk>/', post_delete_view, name='post_delete'),
    path('create/', DashboardBlogCreateView.as_view(), name='post_create')

   ]