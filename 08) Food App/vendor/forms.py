from django import forms
from accounts.models import User,UserProfile
from .models import Vendor,OpeningHours
from accounts.validators import allow_only_images_validate


class VendorForm(forms.ModelForm):
    vender_licence = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
        validators=[allow_only_images_validate]
    )

    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vender_licence']


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ['day','from_hour','to_hour','is_closed']
