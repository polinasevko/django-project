from django.db import models
from django.utils import timezone
from .models import Order


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('total_price'), models.Sum('number_of_item'))
    if cart_data['total_price__sum'] and cart_data['number_of_item__sum']:
        cart.total_price = cart_data['total_price__sum']
        cart.total_number = cart_data['number_of_item__sum']
    else:
        cart.total_price = 0
        cart.total_number = 0
    cart.save()


def check_date(orders):
    for order in orders:
        if order.order_date <= timezone.now():
            order.status = Order.STATUS_COMPLETED
            order.save()
