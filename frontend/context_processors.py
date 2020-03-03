from django.urls import reverse

from catalogue.categories import Category
from cart.tools import check_cart_if_exists_for_context_processor
from site_settings.constants import CURRENCY
from catalogue.models import Product
from accounts.forms import LoginForm


def frontend_site_data(request):
    navbar_categories = Category.browser.navbar().order_by('tree_id', 'level', 'parent')
    parent_categories = Category.browser.parent_categories().order_by('tree_id', 'level', 'parent')
    cart = check_cart_if_exists_for_context_processor(request)
    return {
        'navbar_categories': navbar_categories,
        'parent_categories': parent_categories,
        'user': request.user,
        'cart': cart,
        'currency': CURRENCY,
        'featured_products': Product.my_query.featured_products(),
        'login_form': LoginForm(),
        'eng_title': 'Optika-Kotsalis',
        'eng_url': reverse('eng:homepage'),
        'greek_url': reverse('homepage')
    }