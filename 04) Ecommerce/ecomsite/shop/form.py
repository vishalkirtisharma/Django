from django.forms import forms
from . import models


class AddProduct(models.ProductsModel):
    class Meta:
        model = models.ProductsModel
        fields = '__all__'
        exclude = ['id']
        