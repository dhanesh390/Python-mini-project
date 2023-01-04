from django.contrib import admin

from .models import User, ShopDetail, Product, ShopProduct

# Register your models here.

admin.site.register(User)
admin.site.register(ShopDetail)
admin.site.register(Product)
admin.site.register(ShopProduct)

