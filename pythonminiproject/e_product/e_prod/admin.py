from django.contrib import admin
from .models import User, ShopDetails, Product, ShopProduct

# Register your models here.

admin.site.register(User)
admin.site.register(ShopDetails)
admin.site.register(Product)
admin.site.register(ShopProduct)

