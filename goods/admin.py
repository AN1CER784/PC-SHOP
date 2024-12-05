from django.contrib import admin

from goods.models import Category, Product


@admin.register(Category)
class ModelCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ModelProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    list_filter = ('category',)