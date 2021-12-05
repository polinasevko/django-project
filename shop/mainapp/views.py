from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import CartProduct, Category, Product, Customer, Order
from .mixins import CartMixin
from .forms import OrderForm, LoginForm, SignInForm
from .utils import recalc_cart, check_date


class BaseView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'categories': categories,
            'products': products,
        }
        return render(request, 'base.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        product = self.get_object()
        context['categories'] = categories
        context['specifications'] = product.productfeature_set.all().order_by('feature')
        return context


class CategoryDetailView(DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        categories = Category.objects.all()
        context['category_products'] = category.product_set.all()
        context['categories'] = categories
        return context


class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        product = Product.objects.get(slug=slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product,
        )
        if created:
            # self.cart.products.add(cart_product)
            recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        product = Product.objects.get(slug=slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product,
        )
        # self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class ChangeNumberOfItemsView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        product = Product.objects.get(slug=slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product,
        )
        cart_product.number_of_item = int(request.POST.get('number_of_item'))
        cart_product.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories,
        }
        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'categories': categories,
            'form': form,
            'cart': self.cart,
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            # customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Order is accepted.')
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/checkout/')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories}
        return render(request, 'login.html', context)


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories}
        return render(request, 'sign_in.html', context)

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.password = form.cleaned_data['password']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(user=new_user, phone=form.cleaned_data['phone'])
            # user = authenticate(username=new_user.username, password=new_user.password)
            login(request, new_user)
            return HttpResponseRedirect('/')
        categories = Category.objects.all()
        context = {'categories': categories, 'form': form}
        return render(request, 'sign_in.html', context)


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('order_date')
        categories = Category.objects.all()
        check_date(orders)
        context = {'categories': categories, 'orders': orders}
        return render(request, 'profile.html', context)
