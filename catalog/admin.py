from django.contrib import admin
from django.utils.safestring import mark_safe

from catalog.models import Category, Product, Contact, Version


class DataMixin:
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(DataMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')


@admin.register(Product)
class ProductAdmin(DataMixin, admin.ModelAdmin):
    fields = ['name', 'slug', 'description', 'image', 'post_image', 'category', 'price',
              'is_published', 'views_count',]
    list_display = ('name', 'slug', 'post_image', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    readonly_fields = ('post_image', 'views_count',)

    @admin.display(description='Картинка')
    def post_image(self, product: Product):
        if product.image:
            return mark_safe(f"<img src='{product.image.url}'>")
        return 'Нет картинки'


@admin.register(Contact)
class ContactAdmin(DataMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'phone', 'message')
    list_filter = ('name',)
    search_fields = ('name', 'phone',)


@admin.register(Version)
class VersionAdmin(DataMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'version', 'current_version', 'product')
    list_filter = ('product',)
    search_fields = ('version', 'name',)
