from django.views.generic import View
from .models import Cart, Customer
from django.http import HttpResponseRedirect
from django.contrib import messages


class CartMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(user=request.user)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
            self.cart = cart
            return super(CartMixin, self).dispatch(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, 'You need to authorize.')
            return HttpResponseRedirect('/')
