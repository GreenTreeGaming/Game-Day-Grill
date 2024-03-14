from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from django.views.decorators.csrf import csrf_exempt

from .models import *

from .utils import cookieCart, cartData, guestOrder

def home(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'store/home.html', context)

def cart(request):  
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def events(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'store/events.html', context)

def about(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'store/about.html', context)



def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def appetizers(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.filter(type='A')
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/appetizers.html', context)

def allitems(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/allitems.html', context)

def maincourses(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.filter(type='MC')
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/maincourses.html', context)

def sides(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.filter(type='S')
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/sides.html', context)

def desserts(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.filter(type='D')
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/desserts.html', context)

def extras(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.filter(type='E')
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/extras.html', context)

def contact(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'cartItems': cartItems}
    return render(request, 'store/contact.html', context)
    

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode']
    )

    return JsonResponse('Payment submitted', safe=False)

@csrf_exempt
def processReservation(request):
    data = json.loads(request.body)

    form_data = data['form']

    Reservation.objects.create(
        first_name=form_data['firstName'],
        last_name=form_data['lastName'],
        email=form_data['email'],
        phone=form_data['phoneNumber'],
        party_size=form_data['partySize'],
        special_requests=form_data['specialRequest'],
        time=form_data['time'],
    )

    return JsonResponse('Reservation submitted', safe=False)

def reservation(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'cartItems': cartItems}
    return render(request, 'store/reservation.html', context)