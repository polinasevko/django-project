from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View
from .models import GuitarProduct, PianoProduct, MicProduct, CartProduct, Category, LatestProducts, Customer, Cart
from .mixins import CategoryDetailMixin, CartMixin


class BaseView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_sidebar()
        products = LatestProducts.objects.get_products_for_main_page('guitarproduct', 'pianoproduct', 'micproduct')
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart,
        }
        return render(request, 'base.html', context)


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    CT_MODEL_CLASS = {
        'guitarproduct': GuitarProduct,
        'pianoproduct': PianoProduct,
        'micproduct': MicProduct,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_CLASS[kwargs['content_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        content_model = kwargs.get('content_model')
        slug = kwargs.get('slug')
        content_type = ContentType.objects.get(model=content_model)
        product = content_type.model_class().objects.get(slug=slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id, total_price=product.price
        )
        if created:
            self.cart.products.add(cart_product)
        self.cart.save()
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        content_model = kwargs.get('content_model')
        slug = kwargs.get('slug')
        content_type = ContentType.objects.get(model=content_model)
        product = content_type.model_class().objects.get(slug=slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id,
            #total_price=product.price
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        self.cart.save()
        return HttpResponseRedirect('/cart/')


class ChangeNumberOfItemsView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        content_model = kwargs.get('content_model')
        slug = kwargs.get('slug')
        content_type = ContentType.objects.get(model=content_model)
        product = content_type.model_class().objects.get(slug=slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id,
            #total_price=product.price
        )
        cart_product.number_of_item = int(request.POST.get('number_of_item'))
        cart_product.save()
        self.cart.save()
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories,
        }
        return render(request, 'cart.html', context)


