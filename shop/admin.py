from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['creator', 'name', 'price', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
