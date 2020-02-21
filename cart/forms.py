from django import forms
from django.forms import formset_factory
from django.forms import ModelChoiceField

from .models import Attribute, Cart
from site_settings.models import Shipping, PaymentMethod
from catalogue.models import Product


class EngModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.eng_title}'


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CartForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Cart
        fields = '__all__'
        read_only = ['cart_id']


class CartAttributeForm(forms.Form):
    attributes = forms.ModelChoiceField(queryset=Attribute.objects.all())


CartAttributeFormset = formset_factory(CartAttributeForm, extra=2)


class CheckOutForm(BaseForm):
    first_name = forms.CharField(label='Όνομα *')
    last_name = forms.CharField(label='Επώνυμο *')
    email = forms.EmailField(label='Email *')
    address = forms.CharField(label='Διεύθυνση *')
    city = forms.CharField(label='Πόλη *')
    zip_code = forms.CharField(label='TK *', max_length=5)
    cellphone = forms.CharField(label='Κινητό *')
    phone = forms.CharField(label='Σταθερό τηλέφωνο', required=False)
    notes = forms.CharField(label='Σημειώσεις', widget=forms.Textarea(), required=False)
    shipping_method = forms.ModelChoiceField(required=True, queryset=Shipping.objects.filter(active=True),
                                             label='Τρόπος Μεταφοράς *')
    payment_method = forms.ModelChoiceField(required=True, queryset=PaymentMethod.my_query.active_for_site(),
                                            label='Τρόπος Πληρωμής *', )

    agree = forms.BooleanField(label='Συμφωνώ με τους όρους χρήσης *', widget=forms.CheckboxInput())

    def clean_cellphone(self):
        cellphone = self.cleaned_data.get('cellphone')
        if not str(cellphone).startswith('69'):
            raise forms.ValidationError('Ο αριθμος πρεπει να ξεκινάει από 69')
        return cellphone


class CheckOutEngForm(CheckOutForm):
    shipping_method = EngModelChoiceField(required=True, queryset=Shipping.objects.filter(active=True))
    payment_method = EngModelChoiceField(required=True, queryset=PaymentMethod.my_query.active_for_site())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['address'].label = 'Address'
        self.fields['city'].label = 'City'
        self.fields['zip_code'].label = 'ZipCode'
        self.fields['cellphone'].label = 'Cellphone'
        self.fields['phone'].label = 'Phone'
        self.fields['notes'].label = 'notes'
        self.fields['shipping_method'].label = 'Shipping Method'
        self.fields['payment_method'].label = 'Payment Method'
        self.fields['agree'].label = 'Agree to Rules'

    def clean_phone(self):
        cellphone = self.cleaned_data.get('cellphone')
        return cellphone


class ProductCartForm(BaseForm):
    qty = forms.IntegerField(required=True)

