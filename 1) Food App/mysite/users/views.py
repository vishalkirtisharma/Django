from django.shortcuts import render,redirect
from django.contrib import messages
from . import forms
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request,f'Welcome {user_name}, you account is created')
            return redirect('users:login')
        
        else:
            # Handle invalid form and show errors
            # messages.error(request, 'There was an error with your form. Please check your details and try again.')
            messages.error(request, form.errors)
            return render(request, 'users/register.html', {'form': form})  # Make sure to return the form with errors.



    else:

        form = forms.RegisterForm()
        return render(request,'users/register.html',{'form':form})
    
@login_required
def profilepage(request):
    return render(request,'users/profile.html')