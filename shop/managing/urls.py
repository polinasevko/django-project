from django.urls import path
from .views import *

urlpatterns = [
    path('', BaseManagingView.as_view(), name='base-managing'),
    path('new-category/', CreateNewCategoryView.as_view(), name='new-category'),
    path('new-feature/', CreateNewFeatureView.as_view(), name='new-feature'),
    path('feature-to-product/select-category/', SelectCategoryView.as_view(), name='select-category'),
    path('feature-to-product/', FeatureToProductView.as_view(), name='feature-to-product'),
]
