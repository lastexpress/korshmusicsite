from django.contrib import admin

from .models import Category, Product

@admin.register(Category)
class CategoryShop(admin.ModelAdmin):
	list_display = ('name', 'slug')
	prepopulated_fields = {'slug' : ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('category', 'name', 'slug', 'price', 'available')
	prepopulated_fields = {'slug' : ('name',)}
