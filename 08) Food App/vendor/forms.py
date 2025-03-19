from django import forms
from accounts.models import User,UserProfile
from .models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        
        model = Vendor
        fields = ['vendor_name','vender_licence',]