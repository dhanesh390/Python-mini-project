from django.contrib import admin
from .models import User, ShopDetails, Category, Product

# Register your models here.

admin.site.register(User)
admin.site.register(ShopDetails)
admin.site.register(Category)
admin.site.register(Product)

