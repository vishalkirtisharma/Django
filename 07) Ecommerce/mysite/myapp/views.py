from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse,HttpResponseNotFound
from  . import models
from django.urls import reverse
import json
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from . import forms
from django.db.models import Sum
import datetime
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    products = models.Product.objects.all()

    return render(request, 'myapp/index.html',{
        'products':products,
        'title': 'Home'
    })


def detail_view(request,id):
    product = get_object_or_404(models.Product,id=id)
    stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    return render(request, 'myapp/detail.html',{
        'product':product,
        'stripe_publishable_key':stripe_publishable_key,
        'title': product.name
    })


import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def create_checkout_session(request, id):
    try:
        logger.info(f"Received checkout request for product {id}")
        request_data = json.loads(request.body)
        logger.debug(f"Request data: {request_data}")

        product = get_object_or_404(models.Product, id=id)
        stripe.api_key = settings.STRIPE_SECRET_KEY

        checkout_session = stripe.checkout.Session.create(
            customer_email=request_data['email'],
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(product.price * 100),
                        'product_data': {
                            'name': product.name
                        }
                    },
                    'quantity': 1
                }
            ],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('failed'))
        )

        order = models.OrderDetail()
        order.customer_email = request_data['email']
        order.product = product
        order.stripe_payment_intent = checkout_session.get('payment_intent', checkout_session['id'])
        order.amount = int(product.price)
        order.save()

        return JsonResponse({'sessionId': checkout_session.id})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def payment_sucesss_view(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponseNotFound('Invalid session id')
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    order = get_object_or_404(models.OrderDetail,stripe_payment_intent = session.payment_intent)
    order.has_paid = True

    product = models.Product.objects.get(id=order.product.id)
    product.total_sales_amount += int(product.price)
    product.total_sales += 1

    product.save()

    order.save()
    return render(request,'myapp/payment_success.html',{'order':order})

def payment_failed_view(request):
    return render(request,'myapp/failed.html')

@login_required
def create_product(request):
    product_form = forms.ProductForm()
    title = 'Create Product'

    if request.method == 'POST':
        product_form = forms.ProductForm(request.POST,request.FILES)
        if product_form.is_valid():
            new_product =product_form.save(commit=False)
            new_product.seller = request.user 
            new_product.save()
            return redirect('index')
    return render(request,'myapp/create_product.html',{
        'product_form':product_form,
        'title': title
    })


@login_required
def product_edit(request,id):    
    product = get_object_or_404(models.Product,id=id)
    if product.seller == request.user:
        product_form = forms.ProductForm(request.POST or None,request.FILES or None,instance=product)
        if request.method =='POST':
            if product_form.is_valid():
                product_form.save()
                return redirect('index')
    else:
        return redirect('invalid')
      
    return render(request,'myapp/product_edit.html',{'product_form':product_form,'product':product})

@login_required
def product_delete(request,id):
    product = get_object_or_404(models.Product,id=id)
    if product.seller == request.user:
        if request.method =='POST':
            product.delete()
            return redirect('index')    
    else:
        return redirect('invalid')
    
    return render(request,'myapp/delete.html',{'product':product})

@login_required
def dashboard(request):
    products = models.Product.objects.filter(seller=request.user)

    return render(request,'myapp/dashboard.html',{
        'products':products,
        'title': 'Dashboard'
    })


def register(request):
    if request.method == "POST":
        user_form = forms.UserRegisterationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('index')
        
    user_form = forms.UserRegisterationForm()
    return render(request,'myapp/register.html',{'user_form':user_form})

def invalid(request):
    return render(request,'myapp/invalid.html')

@login_required
def my_purchase(request):
    order = models.OrderDetail.objects.filter(customer_email = request.user.email)
    return render(request,'myapp/purchases.html',{
        'orders':order,
        'title': 'My Purchases'
    })



@login_required
def sales(request):
    title = 'Sales Report'


    orders = models.OrderDetail.objects.filter(product__seller=request.user)
    total_sales = orders.aggregate(Sum('amount'))

    # 365 days sales sum
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = models.OrderDetail.objects.filter(product__seller=request.user,created_on__gt = last_year)
    yearly_sales = data.aggregate(Sum('amount'))

    # 30 days sales sum
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = models.OrderDetail.objects.filter(product__seller=request.user,created_on__gt = last_month)
    monthly_sales = data.aggregate(Sum('amount'))

    # 7 days sales sum
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = models.OrderDetail.objects.filter(product__seller=request.user,created_on__gt = last_week)
    weekly_sales = data.aggregate(Sum('amount'))


    # Daily sales for past 30 days
    daily_orders_sum = (orders.filter(product__seller=request.user).values('created_on').order_by('created_on').annotate(sum=Sum('amount')))
    product_orders_sum = (orders.filter(product__seller=request.user).values('product__name').order_by('product__name').annotate(sum=Sum('amount')))
    
    # datas = {str(i['created_on']) : i['sum'] for i in daily_orders_sum}
    # Convert QuerySet to a dictionary with string dates
    datas =json.dumps( {str(i['created_on']): i['sum'] for i in daily_orders_sum})
    product_data = json.dumps({i['product__name']:i['sum'] for i in product_orders_sum})    



    return render(request,'myapp/sales.html',{
        'title': title,

        'total_sales':total_sales,
        'yearly_sales':yearly_sales,
        'monthly_sales':monthly_sales,
        'weekly_sales':weekly_sales,
        'daily_orders_sums':daily_orders_sum,
        'product_orders_sum':product_orders_sum,
        'datas':datas,
        'product_data':product_data,
        })
