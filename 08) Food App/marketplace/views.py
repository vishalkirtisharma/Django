from django.shortcuts import render
from vendor.models import Vendor
from menu.models import Category,FoodItem

from django.http import HttpResponse
from django.db.models import Prefetch
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from .context_processers import get_cart_amount

# Create your views here.

def marketplace(request):
    vendors   = Vendor.objects.filter(is_approved=True,user__is_active = True)
    vendors_count = vendors.count()
    context ={
        'vendors':vendors,
        'vendors_count':vendors_count
    }
    
    return render(request,'marketplace/listings.html',context)

def vendor_detail(request,slug=None):
    vendor = Vendor.objects.get(slug=slug)
    categories =Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user)
    else:
        cart_item = None
    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_item':cart_item,
        }
    return render(request,'marketplace/vendor_detail.html',context)

from .models import Cart
from marketplace.context_processers import get_cart_counter
def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Checking if request is AJAX
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'success', 'message': 'Item added to cart successfully.','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amount(request)})
                except Cart.DoesNotExist:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'Item added to cart successfully.','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amount(request)})
            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'failed', 'message': 'Food item does not exist.'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please log in to continue'})
    

def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Checking if request is AJAX
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity =0
                        

                    return JsonResponse({'status': 'success', 'cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amount(request)})
                except Cart.DoesNotExist:
                    
                    return JsonResponse({'status': 'failed', 'message': 'You dont have this item in your cart.'})
            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'failed', 'message': 'Food item does not exist.'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please log in to continue'})

@login_required(login_url='logim')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request,'marketplace/cart.html',context)


def delete_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Checking if
            try:
                cart_item = Cart.objects.get(user=request.user,id=cart_id)
                if cart_id:
                    cart_item.delete()
                    return JsonResponse({'status': 'success', 'cart_counter':get_cart_counter(request),'message':'Item has been removed from your cart.','cart_amount':get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'failed', 'message': 'Item does not exist in your cart'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})