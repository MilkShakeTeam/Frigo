from django.contrib import admin
from app.models import Product, Fridge, ProductFridge


class FridgeInline(admin.TabularInline):
    model = Fridge
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [FridgeInline]
    list_display = ('name', 'exp_date', 'need_to_eat')
    list_filter = ['exp_date', 'name']
    search_fields = ['name']

admin.site.register(Fridge)
admin.site.register(ProductFridge)
admin.site.register(Product, ProductAdmin)