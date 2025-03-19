from django.shortcuts import render,redirect
from .forms import VendorForm
from accounts.forms import UserForm
from accounts.models import User,UserProfile
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.

from accounts.utills import detect
from django.core.exceptions import PermissionDenied


def check_role_vendor(user):    
    if user.role==1:
        return True
    else:
        raise PermissionDenied


def check_role_cutomer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied





def registervendor(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already logged in')
        return redirect('dashboard')


    if request.method == 'POST':
        form = UserForm(request.POST)
        vform = VendorForm(request.POST,request.FILES)
        if form.is_valid() and vform.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)

            user.role = User.VENDOR
            user.save()

            vendor = vform.save(commit=False)
            vendor.user = user
            # user_profile = User.objects.get(user=user)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,'Your accounts has been registerd successfully,please wait for the approval')
            print('Your accounts has been registerd successfully,please wait for the approval')
            return redirect('registervendor')
            # user =form.save(commit=False)
            # user.role = models.User.CUSTOMER
            # password = form.cleaned_data['password']
            # user.set_password(password)
            # user.save()

        else:
            print(form.errors)
            print(vform.errors)

    else:

        form = UserForm()
        vform = VendorForm()
 
    context = {
    'form': form,
    'vform': vform
    }

    return render(request, 'accounts/registervendor.html',context=context)



def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already logged in')
        return redirect('myaccounts')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'Now you are loging')
            return redirect('myaccounts')
        else:
            messages.error(request,'Invalid email or password')
            return redirect('login')

    return render(request,'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request,'You are logged out')
    return redirect('login')

def dashboard(request):    
    return render(request,'accounts/dashboard.html')

@login_required(login_url='login')
def myaccounts(request):
    user =request.user
    redirecturl = detect(user)    
    return redirect(redirecturl)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendordashboard(request):
    return render(request,'accounts/vendordashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_cutomer)
def custdashboard(request):
    return render(request,'accounts/custdashboard.html')
