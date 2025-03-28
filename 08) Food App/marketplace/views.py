from django.shortcuts import render
from vendor.models import Vendor
from menu.models import Category,FoodItem


from django.db.models import Prefetch
# Create your views here.

def marketplace(request):
    vendors   = Vendor.objects.filter(is_approved=True,user__is_active = True)
    vendors_count = vendors.count()
    context ={
        'vendors':vendors,
        'vendors_count':vendors_count
    }
    
    return render(request,'marketplace/listings.html',context)

def vendor_detail(reqest,slug=None):
    vendor = Vendor.objects.get(slug=slug)
    categories =Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )


    context = {
        'vendor':vendor,
        'categories':categories,
        }
    return render(reqest,'marketplace/vendor_detail.html',context)