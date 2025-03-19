from django.shortcuts import render,redirect
from . import forms,models
from django.contrib import messages
from .utills import send_verification_email
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
            mail_subject = 'Please Activate your account'
            email_template = 'accounts/emails/account_verification_email.html'

            send_verification_email(request,user,mail_subject,email_template)



            messages.success(request,'Your accounts has been registerd successfully')



            return redirect('registeruser')
        else:
            print(form.errors)

    else:
        form = forms.UserForm()


    return render(request, 'accounts/registeruser.html',{'form':form})

from accounts.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account has been activated.')
        return redirect('myaccounts')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('myaccounts')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            mail_subject = 'Reset your Password'
            email_template = 'accounts/emails/reset_password_email.html'

            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request,'Password Reset link has been sent to your mail address.')
            return redirect('login')
        else:
            messages.error(request,'Accounts dose not exist')
            return redirect('forgot_password')
    

    return render(request,'accounts/forgot_password.html')


def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request,'please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request,'Invalid link')
        return redirect('myaccounts')


    

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
             pk = request.session.get('uid')
             user = User.objects.get(pk=pk)
             user.set_password(password)
             user.is_active = True
             user.save()
             messages.success(request,'Password has been reset')
             return redirect('login')
        
        else:
            messages.error(request,'Password do not match')
            return redirect('reset_password')

    return render(request,'accounts/reset_password.html')