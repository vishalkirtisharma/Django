from django.shortcuts import render,redirect
from marketplace.models import Cart
from marketplace.context_processers import get_cart_amount
from .forms import Orderform
from .models import Order,OrderedFood
# import simplejson as json
import json
# Create your views here.
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from .utills import generate_order_numner
from django.http import HttpResponse

from .models import Payment
from accounts.utills import send_notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from foodonline_main.settings import RAZP_KEY_ID,RAZP_KEY_SECRET

import razorpay

client = razorpay.Client(auth=(RAZP_KEY_ID,RAZP_KEY_SECRET))

@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-created_at')
    cart_count = cart_items.count()
    
    if cart_count <=0:
        return redirect('marketplace')
    subtotal = get_cart_amount(request)['subtotal']
    total_tax = get_cart_amount(request)['tax']
    grand_total = get_cart_amount(request)['grand_total']
    tax_data = get_cart_amount(request)['tax_dict']
    # print(subtotal,total_tax,grand_total,tax_data)
    if request.method == 'POST':
        form = Orderform(request.POST)
        if form.is_valid():
            # Process the order here
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total =grand_total
            order.tax_data = {'1':'1'}
            # order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment-method']
            order.save()

            order.order_number = generate_order_numner(order.id)
            order.save()
                
            # Example order details
            DATA = {
                "amount": float(order.total)*100,  # Amount in paise (₹500.00)
                "currency": "INR",
                "receipt": "receipt #" + order.order_number,
                # "payment_capture": 1  # Auto capture
                'notes':{
                    'key1':'value1',
                    'key2':'value2'
                }
            }

            # Create order
            rzp_order = client.order.create(DATA)
            raz_order_id = rzp_order['id']
            context ={
                'order':order,
                'cart_items':cart_items,
                'raz_order_id':raz_order_id,
                'RZP_KEY_ID':RAZP_KEY_ID,
                'rzp_amount':float(order.total) *100
            }

            return render(request,'orders/place_order.html',context)
        else:
            print(form.errors)
            return render(request, 'orders/place_order.html', {'form': form, 'cart_items': cart_items, 'subtotal': subtotal, 'total_tax': total_tax, 'grand_total': grand_total})
        
    return render(request,'orders/place_order.html')

# send ajax request
@login_required(login_url='login')
def payments(request):
    # check the request is ajaz or not
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method =='POST':

        # store the payment details
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        
        order =Order.objects.get(user=request.user,order_number=order_number)
        payment = Payment(
            user=request.user,
            transaction_id=transaction_id,
            payment_method=payment_method,
            amount= order.total,
            status=status
        )
        payment.save()

        # update the order_model
        order.payment=payment
        order.is_ordered=True
        order.save()


        # move cart_item to ordered food model
        cart_item =Cart.objects.filter(user=request.user)
        
        for item in cart_item:
            order_food = OrderedFood()
            order_food.order = order
            order_food.payment = payment
            order_food.user = request.user
            order_food.fooditem =  item.fooditem
            order_food.quantity = item.quantity
            order_food.price = item.fooditem.price
            order_food.amount = item.fooditem.price * item.quantity # Total Amount
            order_food.save()


        # send order confirmation email to customer
        mail_subject = 'Thanks for ordering with us'
        mail_template = 'orders/order_confirmation_email.html'
        context = {
            'user':request.user,
            'order':order,
            'to_email':order.email
        }
        send_notification(mail_subject,mail_template,context)


        # send order received email to vendor
        mail_subject = 'You have received a new order'
        mail_template = 'orders/new_order_received.html'
        to_email = list(set([i.fooditem.vendor.user.email for i in cart_item]))
        
        print(to_email)
        context ={
            'order':order,
            'to_email': to_email
        }
        send_notification(mail_subject,mail_template,context)

        # clear the cart if payment is suceess
        # cart_item.delete()


        # return HttpResponse('Data Saved email sent')

        # return back to ajax with status of success or failure
        response = {
            'order_number':order_number,
            'transaction_id':transaction_id
        }
        return JsonResponse(response)

    return HttpResponse('Payment View')

def order_complete(request):
    order_number =request.GET.get('order_no')
    transaction_id =request.GET.get('trans_id')

    # try:
    order = Order.objects.get(order_number=order_number,payment__transaction_id=transaction_id,is_ordered=True)
    ordered_food = OrderedFood.objects.filter(order=order)
    subtotal = 0

    # tax_data = json.load(order.tax_data)
    for item in ordered_food:
        subtotal += item.price * item.quantity

    context = {
        'order':order,
        'ordered_food':ordered_food,
        'subtotal':subtotal,
    }

    return render(request,'orders/order_complete.html',context)

    # except:
    #     return redirect('home')
