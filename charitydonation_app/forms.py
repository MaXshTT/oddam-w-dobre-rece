from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from .models import Category, Donation, Institution


class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation
        exclude = ('user',)


class ContactForm(forms.Form):
    name = forms.CharField(required=True, max_length=40, label='')
    surname = forms.CharField(required=True, max_length=40, label='')
    email = forms.EmailField(required=True, max_length=100, label='')
    message = forms.CharField(required=True, widget=forms.Textarea, label='')
