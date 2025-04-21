from django.shortcuts import render
from vendor.models import Vendor
from menu.models import Category,FoodItem

from django.http import HttpResponse
from django.db.models import Prefetch
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from .context_processers import get_cart_amount
from django.db.models import Q
from datetime import date,datetime
# Create your views here.

def marketplace(request):
    vendors   = Vendor.objects.filter(is_approved=True,user__is_active = True)
    vendors_count = vendors.count()
    context ={
        'vendors':vendors,
        'vendors_count':vendors_count
    }
    
    return render(request,'marketplace/listings.html',context)

from vendor.models import OpeningHours
def vendor_detail(request,slug=None):
    vendor = Vendor.objects.get(slug=slug)
    categories =Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )


    opening_hours = OpeningHours.objects.filter(vendor=vendor).order_by('day','-from_hour')
    # check current day opening hours
    today = date.today().isoweekday()
    current_opening_hours = OpeningHours.objects.filter(vendor=vendor,day=today)
    # current_time = datetime.now().strftime('%H : %M: %S')

    
    # is_open=None

    # for i in  current_opening_hours:
    #     start = str( datetime.strptime(i.from_hour,'%I:%M %p').time())
    #     end = str (datetime.strptime(i.to_hour,'%I:%M %p').time())
    #     if current_time > start and current_time < end:
    #         is_open = True
    #         break
    #     else:
    #         is_open = False
    

    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user)
    else:
        cart_item = None
    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_item':cart_item,
        'opening_hours':opening_hours,
        'current_opening_hours':current_opening_hours,
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
        
    
def search(request):
    address= request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']

    # get vedor ids that has the food item the user is looking for
    fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword,is_available=True).values_list('vendor',flat=True)
    print(fetch_vendors_by_fooditems)
    vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems)| Q(vendor_name__icontains=keyword,is_approved=True,user__is_active=True))

    # vendors   = Vendor.objects.filter(vendor_name__icontains=keyword,is_approved=True,user__is_active=True)

    vendor_count = vendors.count()
    context ={
        'vendors':vendors,
        'vendor_count':vendor_count,
        }

    return render(request,'marketplace/listings.html',context)