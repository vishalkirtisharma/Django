from django import forms
from . import models
class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = models.User
        fields = [
                    'first_name',
                    'last_name',
                    'username',
                    'email',
                    'phone_number',
                    'password'
                    ]
        
    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get('passw ord')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data
