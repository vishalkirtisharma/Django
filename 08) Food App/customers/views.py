from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 
from accounts.forms import UserProfileForm,UserInfoForm
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.contrib import messages

from orders.models import Order,OrderedFood
# Create your views here.
@login_required(login_url='login')
def cprofile(request):
    profile = get_object_or_404(UserProfile,user = request.user)
    if request.method =='POST':
        
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        user_form =UserInfoForm(request.POST,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Profile Update')
            return redirect('cprofile')
        else:
            messages.error(request, 'Please correct the errors below.')
            return redirect('cprofile')

        
    else:

        profile_form = UserProfileForm(instance=profile)
        user_form =UserInfoForm(instance=request.user)

    context = {
        'profile_form': profile_form, 
        'user_form': user_form,
        'profile': profile
    }

    return render(request,'customers/cprofile.html',context)


# def my_orders(request):
#     orders = Order.objects.filter(user=request.user,is_ordered=True ).order_by('-created_at')
#     context = {'orders':orders}
#     return render(request,'customers/my_orders.html',context)

from django.core.paginator import Paginator

def my_orders(request):
    orders_list = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    paginator = Paginator(orders_list, 10)  # 10 orders per page

    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    start_index = (orders.number - 1) * paginator.per_page + 1
    end_index = start_index + len(orders.object_list) - 1
    total_orders = paginator.count

    context = {
        'orders': orders,
        'start_index': start_index,
        'end_index': end_index,
        'total_orders': total_orders,
    }
    return render(request, 'customers/my_orders.html', context)


def order_details(request,order_number=None):
    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal = (item.price*item.quantity)

        context = {
            'order':order,
            'ordered_food':ordered_food,
            'subtotal':subtotal
        }

        return render(request,'customers/order_details.html',context)

    except:
        return redirect('customer')

    