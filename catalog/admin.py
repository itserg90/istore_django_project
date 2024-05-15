from django.contrib import admin

from catalog.models import Category, Product, Contacts, Blog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'image', 'is_published')
    list_filter = ('title', 'is_published',)
    search_fields = ('title',)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('country', 'inn', 'adress')
