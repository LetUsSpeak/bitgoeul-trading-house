from django import forms
from django.forms import ModelForm

from productapp.models import Product


class ProductCreationForm(ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'editable',
                                                           'style': 'text-align: left'
                                                                    'min-height: 10rem'}))

    class Meta:
        model = Product
        fields = ['name', 'price', 'market_name', 'head_image']
