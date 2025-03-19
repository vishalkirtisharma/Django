from django.shortcuts import render,redirect
from . import forms,models
from django.contrib import messages
# Create your views here.
def registeruser(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already logged in')
        return redirect('dashboard')

    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.role = models.User.CUSTOMER
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.success(request,'Your accounts has been registerd successfully')



            return redirect('registeruser')
        else:
            print(form.errors)

    else:
        form = forms.UserForm()


    return render(request, 'accounts/registeruser.html',{'form':form})
