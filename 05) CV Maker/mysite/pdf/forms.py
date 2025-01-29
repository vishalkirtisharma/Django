from django import forms
from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.ProfileModel
        fields = '__all__'

