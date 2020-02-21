from django.conf.urls import url
from django.urls import path ,re_path
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap

from .views_eng import (HomepageView, OfferView, SearchView, BrandListView, CategoryView, ProductView, BrandDetailView,
                        newsletter_form_view, NewProductsListView)

from .user_views_eng import (UserDashboardView, login_view, register_view, fast_login_view,
                             account_activation_sent, activate, update_profile_view, change_password_view, UserProfileOrderListView,
                             add_product_to_wishlist_view, WishlistListView,  remove_from_wishlist_view, user_personal_data_view,
                             delete_user_view, pdf_user_data_view
                             )
from .cart_checkout_eng_view import CartPageView, add_product_to_cart, delete_product_from_cart, CheckoutView, order_success_url, OrderDetailView, add_product_with_attr_to_cart, add_voucher_to_cart_view, delete_voucher_from_cart_view, decide_what_to_do_with_order_payment

from .ajax_views import ajax_search_brands, ajax_change_cart_item_qty, ajax_check_voucher, ajax_change_cart_attribute_qty, ajax_add_product_modal, ajax_quick_modal_view, ajax_delete_cart_item, ajax_estimate_costs, ajax_update_cate_shipping_method_view
from .footer_views_eng import ShippingListView, PaymentMethodListView, order_status_form_view, TermsView, ReturnProductPolicyView, CompanyView, ContactView, PersonalDataView

from .paypall_views import payment_canceled, payment_done, payment_process


app_name = 'eng'


urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('search/', SearchView.as_view(), name='search_page'),
    path('offers/', OfferView.as_view(), name='offer_view'),
    path('new-products/', NewProductsListView.as_view(), name='new_products_view'),
    url(r'^category/(?P<slug>[-\w]+)/$', CategoryView.as_view(), name='category_page'),
    path('brands/', BrandListView.as_view(), name='brands_view'),
    path('brand/detail/<slug:slug>/', BrandDetailView.as_view(), name='brand_detail_view'),
    path('cart/', CartPageView.as_view(), name='cart_view'),
    re_path(r'^product/(?P<slug>[-\w]+)/$', ProductView.as_view(), name='product_view'),
    path('newsletter/form/submit/', newsletter_form_view, name='newsletter_form_view'),


    # cart and checkout_paged
    re_path('^προσθήκη-στο-καλάθι/(?P<slug>[-\w]+)/', add_product_to_cart, name='add_to_cart'),
    url(r'^προσθήκη-στο-καλάθι-με-μεγεθολογιο/(?P<slug>[-\w]+)/$', add_product_with_attr_to_cart, name='add_to_cart_with_attr'),
    path('voucher/add/', add_voucher_to_cart_view, name='add_voucher_cart_view'),
    path('voucher/delete/<int:pk>/', delete_voucher_from_cart_view, name='delete_voucher_from_cart'),
    path('διαγραφή-από-το-cart/<int:pk>', delete_product_from_cart, name='delete_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout_view'),
    path('decide-payment', decide_what_to_do_with_order_payment, name='decide_payment_process'),
    path('πραγματοποίηση-παραγγελίας/', order_success_url, name='order_success_url'),

    #  user pages
    path('login/', login_view, name='login'),
    path('fast-login/', fast_login_view, name='fast_login'),
    path('create-account/', register_view, name='register_view'),
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    path('profile/', UserDashboardView.as_view(), name='user_profile'),
    path('edit-profile/', update_profile_view, name='update_profile_view'),
    path('change-password/', change_password_view, name='change_password_view'),
    path('profile/all-orders/', UserProfileOrderListView.as_view(), name='user_profile_order_list'),
    path('profile/order-detail/<slug:slug>/', OrderDetailView.as_view(), name='frontend_order_detail'),
    url(r'^wish-list/add-or-remove/(?P<slug>[-\w]+)/', add_product_to_wishlist_view, name='add_product_wishlist'),
    url(r'^wish-list/remove/(?P<slug>[-\w]+)/', remove_from_wishlist_view, name='remove_product_wishlist'),
    path('wist-list/', WishlistListView.as_view(), name='wishlist'),


    # footer pages
    path('shipping-methods/', ShippingListView.as_view(), name='shipping_list_view'),
    path('payment-types/', PaymentMethodListView.as_view(), name='payment_list_view'),
    path('terms of use/', TermsView.as_view(), name='terms_rules_view'),
    path('our-company/', CompanyView.as_view(), name='company_view'),
    path('policy-of-return/', ReturnProductPolicyView.as_view(), name='return_policy_view'),
    path('order_status/', order_status_form_view, name='order_status_form'),
    path('contact/', ContactView.as_view(), name='contact_view'),
    path('personal-data/', PersonalDataView.as_view(), name='personal_data_view'),
    path('user/personal-data/', user_personal_data_view, name='user_personal_data'),
    path('user/personal-data/pdf/download/', pdf_user_data_view, name='personal_data_pdf_download'),
    path('user/delete/', delete_user_view, name='delete_user'),


    # ajax urls
    path('ajax/search-brands/', ajax_search_brands, name='ajax_search_brands'),
    path('ajax/cart/modify-order-item/<int:pk>/', ajax_change_cart_item_qty, name='ajax_modify_qty'),
    path('ajax/check-voucher/', ajax_check_voucher, name='ajax_check_voucher'),
    path('ajax/cart-attribute/<int:pk>/', ajax_change_cart_attribute_qty, name='ajax_modify_attribute_qty'),
    url(r'^ajax/add-product-modal/(?P<slug>[-\w]+)/$', ajax_add_product_modal, name='ajax_add_product_modal'),
    url(r'^ajax/quick-product-view/(?P<slug>[-\w]+)/$', ajax_quick_modal_view, name='ajax_quick_modal_view'),
    path('ajax/delete/<int:pk>/<slug:action>/', ajax_delete_cart_item, name='ajax_delete_view'),
    path('ajax/estimate/costs/<slug:action>/', ajax_estimate_costs, name='ajax_estimate_cost'),
    path('ajax/checkout-update-prices/', ajax_update_cate_shipping_method_view, name='ajax_checkout_update_cart'),

    #  paypall

    path('paypal_/process/', payment_process, name='paypall_process'),
    path('paypal_/done/', payment_done, name='paypal_done'),
    path('paypal_/canceled/', payment_canceled, name='paypal_canceled'),





]






