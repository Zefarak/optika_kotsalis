from django.views.generic import TemplateView, FormView, ListView, CreateView
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, reverse, render
from django.urls import reverse_lazy
from site_settings.models import PaymentMethod, Shipping
from .forms import OrderStatusEngForm
from point_of_sale.models import Order
from contact.models import Contact
from contact.forms import ContactFrontEndEngForm


def order_status_form_view(request):
    page_title = 'Track Order'
    form = OrderStatusEngForm(request.GET or None)
    if form.is_valid():
        order_code = form.cleaned_data.get('order_code')
        qs = Order.objects.filter(number=order_code) if order_code else Order.objects.none()
        order = qs.first() if qs.exists() else None
        if order:
            return HttpResponseRedirect(reverse('eng:frontend_order_detail', kwargs={'slug': order.number}))
        else:
            messages.warning(request, 'We cant find a order with this code.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request,
                  'frontend_eng/footer_views/order_status_form.html',
                  context={'form': form,
                           'page_title': page_title}
                  )


class PaymentMethodListView(ListView):
    model = PaymentMethod
    template_name = 'frontend_eng/footer_views/payment_policy_view.html'

    def get_queryset(self):
        qs = PaymentMethod.objects.filter(active=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super(PaymentMethodListView, self).get_context_data(**kwargs)
        page_title, keywords, seo_description = 'Τρόποι Πληρωμής', '', ''

        context.update(locals())
        return context


class ShippingListView(ListView):
    model = Shipping
    template_name = 'frontend_eng/footer_views/shipping_policy_view.html'

    def get_queryset(self):
        qs = Shipping.objects.filter(active=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ShippingListView, self).get_context_data(**kwargs)
        page_title, keywords, seo_description = 'Shipping Methods', '',''
        context.update(locals())
        return context


class ReturnProductPolicyView(TemplateView):
    template_name = 'frontend_eng/footer_views/return_policy_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Return Policy'
        return context


class TermsView(TemplateView):
    template_name = 'frontend_eng/footer_views/rules_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Terms of use'
        return context


class CompanyView(TemplateView):
    template_name = 'frontend_eng/footer_views/company_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Our Company'
        return context


class PersonalDataView(TemplateView):
    template_name = 'frontend_eng/footer_views/personal_data.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Personal Data'
        return context


class ContactView(CreateView):
    model = Contact
    form_class = ContactFrontEndEngForm
    template_name = 'frontend_eng/footer_views/contant_view.html'
    success_url = reverse_lazy('contact_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Contact'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your message is saved. We will try to communicate as soon as possible.')
        return super(ContactView, self).form_valid(form)
