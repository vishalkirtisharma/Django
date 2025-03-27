from django.shortcuts import render,redirect,get_object_or_404
from .forms import VendorForm
from accounts.forms import UserForm
from accounts.models import User,UserProfile
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.utills import send_verification_email
from . import models
from accounts.forms import UserProfileForm
# Create your views here.

from accounts.utills import detect
from django.core.exceptions import PermissionDenied

from menu.models import Category,FoodItem
from menu.forms import CategoryForm,FoodItemForm

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


def vendor_required(view_fun):
    def _wrapped_view(request,*args,**kwargs): 
        vendor = models.Vendor.objects.get(user=request.user)
        request.vendor = vendor
        return view_fun(request,*args,**kwargs)
    return _wrapped_view
    


# def get_vendor(request):
#     vendor = models.Vendor.objects.get(user=request.user)



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

            
            mail_subject = 'Please Activate your account'
            email_template = 'accounts/emails/account_verification_email.html'

            send_verification_email(request,user,mail_subject,email_template)



            

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


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(models.Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('vprofile')
        else:
            messages.error(request, 'Invalid form data')
            return redirect('vprofile')
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
@vendor_required
def menu_builder(request):
    # print(request.user)
    vendor  =request.vendor
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,

    } 
    return render(request,'vendor/menu_builder.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
@vendor_required
def fooditems_by_category(request,pk=None):
    vendor  =request.vendor
    category = Category.objects.get(pk=pk)
    fooditems= FoodItem.objects.filter(vendor=vendor,category=category)
    
    context = {
        'fooditems': fooditems,
        'category': category,
    }

    return render(request,'vendor/food_item_by_category.html',context)

from django.template.defaultfilters import slugify

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
@vendor_required
def add_category(request):
    forms = CategoryForm()
    if request.method == 'POST':
        forms = CategoryForm(request.POST)
        if forms.is_valid():
            category_name = forms.cleaned_data['category_name']
            category = forms.save(commit=False)
            category.vendor = request.vendor
            category.slug = slugify(category_name)

            forms.save()
            messages.success(request,'Category added to user')

            return redirect('menu_builder')

    context = {
            'forms': forms,
            }

    return render(request,'vendor/add_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
@vendor_required
def edit_category(request,pk=None):
    category = Category.objects.get(pk=pk)

    forms = CategoryForm(instance=category)
    if request.method == 'POST':
        forms = CategoryForm(request.POST,instance=category)
        if forms.is_valid():
            category_name = forms.cleaned_data['category_name']
            category = forms.save(commit=False)
            category.vendor = request.vendor
            category.slug = slugify(category_name)

            forms.save()
            messages.success(request,'Category update successfully')

            return redirect('menu_builder')

    context = {
            'forms': forms,
            'category':category
            }
    return render(request,'vendor/edit_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request,pk=None):
    category = Category.objects.get(pk=pk)
    category.delete()
    messages.success(request,'Category deleted successfully')
    return redirect('menu_builder')



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
@vendor_required
def add_food(request):
    if request.method == 'POST':
        forms = FoodItemForm(request.POST,request.FILES)
        if forms.is_valid():
            foodtitle  =forms.cleaned_data['food_title']
            food = forms.save(commit=False)
            food.vendor = request.vendor
            food.slug = slugify(foodtitle)
            food.save()
            
            messages.success(request,'Food added successfully')
            return redirect('fooditems_by_category',food.category.id)
        else:
            messages.error(request,'Invalid form')

    else:
        forms = FoodItemForm()
        # modify this form
        forms.fields['category'].queryset = Category.objects.filter(vendor = request.vendor)

        context = {
            'forms': forms
            }
    return render(request,'vendor/add_food.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
@vendor_required
def edit_food(request,pk=None):
    food = FoodItem.objects.get(pk=pk)

    if request.method == 'POST':
        forms = FoodItemForm(request.POST,request.FILES,instance=food)
        if forms.is_valid():
            foodtitle  =forms.cleaned_data['food_title']
            food = forms.save(commit=False)
            food.vendor = request.vendor
            food.slug = slugify(foodtitle)
            food.save()
            
            messages.success(request,'Food updated successfully')
            return redirect('fooditems_by_category',food.category.id)
        else:
            messages.error(request,'Invalid form')

    else:
        forms = FoodItemForm(instance=food)
        forms.fields['category'].queryset = Category.objects.filter(vendor = request.vendor)
        context = {
            'forms': forms,
            'food': food,
            }
    return render(request,'vendor/edit_food.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request,pk=None):
    food = FoodItem.objects.get(pk=pk)
    food.delete()
    messages.success(request,'Food deleted successfully')
    return redirect('fooditems_by_category',food.category.id)

