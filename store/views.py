import datetime

from django.shortcuts import render
from django.http import JsonResponse
from .models import OrderItem, ShippingAddress, Product, Order, Customer
import json
from .utils import cookieCart, cartData, guessOrder


def store(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['item']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['item']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['item']
    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'store/checkout.html', context)


def updateItem(request):
    """ the data we are loading was sent from cart.js which i created for the
    add to cart functionality the reason why we created
    """
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)
    customer = request.user.customer
    """ the reason why we are using get or create is because if the item already 
    exist we just want to add to it or sub
    so what is happening here is that we are getting the productid from cart js then 
    we getting an order or creating one then we are alson getting or creating an orderitem
    """
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,
                                                 complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,
                                                         product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode']
            )
    else:
        customer, order = guessOrder(request, data)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

    return JsonResponse('payment complete', safe=False)
