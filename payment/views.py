# import braintree
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from orders.models import Order,OrderItem
from django.conf import settings

from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
import juspayp3 as Juspay
from random import randint
import json
import razorpay


client =razorpay.Client(auth=(settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY_SECRET_KEY))
client.set_app_details({"title" : "Django", "version" : "1.8.17"})
amount=0
def create_order(request):
    order_id=request.session.get('order_id')
    order=get_object_or_404(Order,id=order_id)
    amount=int(order.get_total_cost()*100)
    amount_inr=amount//100
    print("Type amount ",amount)
    print("Type amount ",type(amount))
    print("Order is -> ",order)
    return render(request,'payment/created.html',{'order_id':order_id,'public_key':settings.RAZORPAY_PUBLIC_KEY,'amount':amount_inr,'amountorig':amount})

def payment_process(request):
    order_id=request.session.get('order_id')
    order=get_object_or_404(Order,id=order_id)
    print("Payment",order)
    if request.method=="POST":
        order.paid=True
        
        order.save()
        print("Payment order",order.paid)
        orderitem=get_object_or_404(OrderItem,order=order)
        print("Order Item",orderitem.get_cost())
        amount=int(orderitem.get_cost())*100
        amount_inr=amount//100
        print("Amount ",amount)
        print("Type amount str to int ",amount)
        payment_id=request.POST['razorpay_payment_id']
        order.braintree_id=payment_id
        order.save()
        # print("Multiple value",payment_id)
        print("Payment Id",payment_id)
        payment_client_capture=(client.payment.capture(payment_id,amount))    
        print("Payment Client capture",payment_client_capture)
        payment_fetch=client.payment.fetch(payment_id)
        status=payment_fetch['status']
        amount_fetch=payment_fetch['amount']
        amount_fetch_inr=amount_fetch//100
        print("Payment Fetch",payment_fetch['status'])
        return render(request,'payment/done.html',{'amount':amount_fetch_inr,'status':status})   

def payment_done(request):
    return render(request, 'payment/done.html',{})
 
 
def payment_canceled(request):
    return render(request, 'payment/canceled.html',{})

def response(request):
    res=dict()
    res['order_id']=request.GET.get('order_id')
    res['status']=request.GET.get('status')
    res['signature']=request.GET.get('signature')
    res['signature_algorithm'] = request.GET.get('signature_algorithm')
    print(res)
    return render(request,'payment/done.html',{'res':res})