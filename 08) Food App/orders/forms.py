from django import forms
from . import models

class Orderform(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['first_name','last_name','phone','email','address','country','state','city','pin_code']