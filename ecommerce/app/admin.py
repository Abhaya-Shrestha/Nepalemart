from django.contrib import admin
from .models import *


# Register your models here.

class Product_Images(admin.TabularInline):
    model = Product_Image


class Additional_informations(admin.TabularInline):
    model = Additional_Information


class Product_admin(admin.ModelAdmin):
    inlines = (Product_Images, Additional_informations)
    list_display = ('product_name', 'price', 'Categories', 'section')
    list_editable = ('Categories', 'section')


class OrderItemTubleinline(admin.TabularInline):
    model = OrdersItem


class OrdersAdmin(admin.ModelAdmin):
    inlines = [OrderItemTubleinline]
    list_display = ['firstname','phone','email','paid','date']


admin.site.register(Slider)
admin.site.register(banner_area)
admin.site.register(Main_category)
admin.site.register(Category)
admin.site.register(Sub_category)

admin.site.register(Section)
admin.site.register(Product, Product_admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)

# admin.site.register(Coupon_Code)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrdersItem)
