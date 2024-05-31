from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ('views_count',)
    list_display = ('title', 'content', 'image', 'is_published',)
    list_filter = ('title', 'is_published',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
