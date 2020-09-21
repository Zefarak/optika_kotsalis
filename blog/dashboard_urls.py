from django.urls import path

from .views import (DashboardBlogListView, DashboardBlogCreateView, DashboardBlogUpdateView, post_delete_view,
                    validate_category_edit_or_delete_view, ajax_update_category_view, validate_category_creation_view
                    )

app_name = 'dashboard_blog'

urlpatterns = [
    path('list/', DashboardBlogListView.as_view(), name='post_list'),
    path('detail/<int:pk>/', DashboardBlogUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', post_delete_view, name='post_delete'),
    path('create/', DashboardBlogCreateView.as_view(), name='post_create'),

    path('validate-category-update-create/<int:pk>/<slug:action>/', validate_category_edit_or_delete_view,
         name='category_update_delete'),

    path('ajax-update-category/<int:pk>/', ajax_update_category_view, name='ajax_update_category'),
    path('validate-category-creation/', validate_category_creation_view, name='validate_category_create'),

   ]