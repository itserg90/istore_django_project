from django.urls import path
from django.views.decorators.cache import cache_page
from catalog.views import *
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('product/create', ProductCreateView.as_view(), name='product_create'),
    path('product/<slug:slug>/update', ProductUpdateView.as_view(), name='product_update'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),
    path('categories/', CategoryListView.as_view(), name='categories'),
]
