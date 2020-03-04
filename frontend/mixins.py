from django.urls import reverse
from django.views.generic import FormView
from django.shortcuts import HttpResponseRedirect
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth import authenticate, login
from django.contrib import messages
from urllib.parse import urlencode
from accounts.forms import LoginForm

from catalogue.categories import Category
from catalogue.product_details import Brand, Color
from catalogue.product_attritubes import Attribute, Characteristics, ProductCharacteristics, CharacteristicsValue
from catalogue.models import Product


from .tools import category_filter_data, get_colors_from_queryset


def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    params = urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


class SearchMixin:

    def get(self, *args, **kwargs):
        if 'search_name' in self.request.GET:
            search_name = self.request.GET.get('search_name')
            return custom_redirect('search_page', search_name=search_name)
        return super(SearchMixin, self).get(*args, **kwargs)


class ListViewMixin(MultipleObjectMixin):
    paginate_by = 16

    def get_paginate_by(self, queryset):
        max_products = self.request.GET.get('max_products', self.paginate_by)
        if max_products in ['16', '32', 64]:
            return max_products
        return self.paginate_by

    def get_queryset(self):
        qs = self.model.my_query.active_for_site()
        self.initial_queryset = qs
        qs = self.model.filters_data(self.request, qs)
        if self.request.GET.getlist('attr_name', None):
            qs = Attribute.product_filter_data(self.request, qs)
        if self.request.GET.getlist('char_name', None):
            try:
                ids = ProductCharacteristics.filters_data(self.request,
                                                          ProductCharacteristics.objects.all()).values_list(
                    'product_related__id')
                qs = qs.filter(id__in=ids)
            except:
                qs = qs
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # seo data
        page_title, description = 'Fixed it', 'Test'

        # filters
        categories, brands = category_filter_data(self.initial_queryset)
        colors = get_colors_from_queryset(self.initial_queryset)
        characteristics_filters = Characteristics.browser.filter_access()
        get_chars = ProductCharacteristics.objects.filter(product_related__in=self.object_list)
        chars_filters = []
        chars_filters_eng = []
        for char in characteristics_filters:
            new_qs = get_chars.filter(title=char)
            new_qs_values = new_qs.values_list('value', 'value__title').distinct()
            chars_filters.append((char.title, new_qs_values))
            new_qs_values_eng = new_qs.values_list('value', 'value__eng_title').distinct()
            chars_filters_eng.append((char.str_eng, new_qs_values_eng))

        qs_attributes = Attribute.objects.filter(class_related__product_related__in=self.object_list)
        attributes = qs_attributes.values_list('title', 'title__name').distinct().order_by('class_related')
        low, max = 0, self.initial_queryset.order_by('-final_price')[0].final_price if self.initial_queryset else 200
        price_name = self.request.GET.get('price_name', '')
        low_selected, max_selected = low, max
        if ';' in price_name:
            low_selected, max_selected = price_name.split(';')
        # create get params for infinite scroll
        get_params = urlencode(self.request.GET)
        infinite_next_point = f'?{get_params}'
        print(chars_filters_eng)
        context.update(locals())
        return context

