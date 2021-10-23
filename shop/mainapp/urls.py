from django.urls import path, include
from .views import BaseView, ProductDetailView, AddToCartView, CategoryDetailView, CartView


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:content_model>/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:content_model>/<str:slug>', AddToCartView.as_view(), name='add-to-cart'),
]
