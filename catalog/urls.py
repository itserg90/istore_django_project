from django.urls import path
from catalog.views import ProductListView, ProductDetailView, ContactTemplateView, ProductCreateView, ProductUpdateView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create', ProductCreateView.as_view(), name='product_create'),
    path('product/<slug:slug>/update', ProductUpdateView.as_view(), name='product_update'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),
]
