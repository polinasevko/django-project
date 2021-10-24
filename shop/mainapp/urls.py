from django.urls import path
from .views import BaseView, ChangeNumberOfItemsView, CheckoutView, DeleteFromCartView, ProductDetailView, AddToCartView, CategoryDetailView, CartView


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:content_model>/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:content_model>/<str:slug>', AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<str:content_model>/<str:slug>', DeleteFromCartView.as_view(), name='remove-from-cart'),
    path('change-number-of-item/<str:content_model>/<str:slug>', ChangeNumberOfItemsView.as_view(), name='change-number-of-item'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
