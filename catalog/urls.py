from django.urls import path
from catalog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('product/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('product/create/', BlogCreateView.as_view(), name='blog_create'),
    path('product/<int:pk>/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('product/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete')
]
