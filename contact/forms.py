from django import forms

from .models import Contact
from site_settings.forms import BaseForm


class ContactForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'


class ContactFrontEndForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number', 'message']


class ContactFrontEndEngForm(ContactFrontEndForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Full Name'
        self.fields['phone_number'].label = 'Phone Number'
        self.fields['message'].label = 'Message'