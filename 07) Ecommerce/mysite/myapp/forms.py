from django import forms
from . import models
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'

class UserRegisterationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email','first_name']

    def check_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Password fields do not match')
        return self.cleaned_data['password']



