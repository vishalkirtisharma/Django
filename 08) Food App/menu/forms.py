from django import forms
from .models import Category,FoodItem
from accounts import validators

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name','description',)


class FoodItemForm(forms.ModelForm):
    image= forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}),validators=[validators.allow_only_images_validate])
    class Meta:
        model = FoodItem
        fields = ('food_title','description','price','category','image','is_available')
        