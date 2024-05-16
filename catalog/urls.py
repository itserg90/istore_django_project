from django.urls import path
from catalog.views import ProductListView, ProductDetailView, ContactTemplateView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),
]
