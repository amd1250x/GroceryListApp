from django import forms
from .models import *


class GroceryListForm(forms.Form):
    name = forms.CharField(max_length=30)
    buyer = forms.CharField(max_length=255)

class ItemForm(forms.Form):
    name = forms.CharField(max_length=255)
    quantity = forms.IntegerField()
    price = forms.DecimalField(max_digits=4, decimal_places=2)

class PersonForm(forms.Form):
    name = forms.CharField(max_length=255)

class PersonToItemForm(forms.Form):
    name_p2i = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'list':'namelist'}))