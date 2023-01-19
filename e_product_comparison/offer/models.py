from django.db import models

from product.models import Product
from shop.models import Shop
from user.models import User


# Create your models here.
class Offer(models.Model):
    """ this class is implemented to maintain the relationship between various product and various shops"""
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shop_product')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_product')
    actual_price = models.FloatField(default=0)
    offer_percentage = models.FloatField(default=0)
    vendor_price = models.FloatField(default=0)
    product_url = models.URLField(max_length=2000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='shop_product_created_user')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='shop_product_updated_user')

    def __str__(self):
        return f'{self.product} {self.id}'
