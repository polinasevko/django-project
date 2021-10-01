from django.urls import path, include
from .views import test_view, ProductDetailView


urlpatterns = [
    path('', test_view, name='base'),
    path('products/<str:content_model>/<str:slug>', ProductDetailView.as_view(), name='product_detail')
]
