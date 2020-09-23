from django.urls import path

from .views import (DashboardBlogListView, DashboardBlogCreateView, DashboardBlogUpdateView, post_delete_view,
                    validate_category_edit_or_delete_view, ajax_update_category_view, validate_category_creation_view,
                    ajax_update_tag_view, validate_tag_creation_view, validate_update_or_delete_tag_view,
                    validate_post_image_creation_view, delete_image_view, ajax_image_modal_view, validate_post_image_update_view
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

    path('validate-tag-creation/', validate_tag_creation_view, name='validate_tag_create'),
    path('validate-tag-edit-or-update/<int:pk>/<slug:action>/', validate_update_or_delete_tag_view, name='validate_tag_edit_or_update'),
    path('ajax-update/tag/<int:pk>/', ajax_update_tag_view, name='ajax_update_tag'),

    path('validate-post-image-view/<int:pk>/', validate_post_image_creation_view, name='validate_post_image'),
    path('delete-image-view/<int:pk>/', delete_image_view, name='delete_image_view'),
    path('ajax-image-update/modal/<int:pk>/', ajax_image_modal_view, name='ajax_image_modal_view'),
    path('validate-update-post-image/<int:pk>/', validate_post_image_update_view, name='validate_update_post_image')

   ]