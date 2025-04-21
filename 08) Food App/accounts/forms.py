from django import forms
from . import models,validators


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
    
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))

    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[validators.allow_only_images_validate])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[validators.allow_only_images_validate])


    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = models.UserProfile
        # fields = ['profile_picture','cover_photo','address_line_1','address_line_2','country','state','city','pin_code','latitude','longitude']
        fields = ['profile_picture','cover_photo','address','country','state','city','pin_code','latitude','longitude']

    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name',  'phone_number']
