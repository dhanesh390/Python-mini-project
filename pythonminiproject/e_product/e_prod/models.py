import uuid
from enum import Enum

from django.db import models
from django.db.models import JSONField


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=25)

    # ADMIN = 'admin'
    # CONSUMER = 'consumer'
    # USER_ROLES = [
    #     (ADMIN, 'admin'),
    #     (CONSUMER, 'consumer')
    # ]
    class Role(models.TextChoices):
        consumer = 'consumer',
        admin = 'admin'

    user_role = models.TextField(choices=Role.choices, default='consumer')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, editable=False, default=None, null=True)
    updated_by = models.CharField(max_length=100, editable=False, default=None, null=True)

    def __str__(self):
        return self.user_name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, unique=True)
    product_price = models.FloatField(default=0)
    product_description = models.TextField(max_length=200)

    class Category(models.TextChoices):
        mobile = 'mobile'
        laptop = 'laptop'
        tv = 'tv'

    product_category_type = models.TextField(choices=Category.choices, default='Null')
    ram = models.CharField(max_length=100, null=True)
    battery = models.CharField(max_length=100, null=True)
    internal_storage = models.CharField(max_length=100, null=True)
    front_camera = models.CharField(max_length=100, null=True)
    external_storage = models.CharField(max_length=100, null=True)
    back_camera = models.CharField(max_length=100, null=True)
    cpu = models.CharField(max_length=100, null=True)
    gpu = models.CharField(max_length=100, null=True)
    display = models.CharField(max_length=100, null=True)
    screen_size = models.CharField(max_length=100, null=True)
    screen_resolution = models.CharField(max_length=100, null=True)
    no_of_speakers = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, editable=False, default=None, null=True)
    updated_by = models.CharField(max_length=100, editable=False, default=None, null=True)

    def __str__(self):
        return self.product_name


class ShopDetails(models.Model):
    shop_id = models.AutoField(primary_key=True)
    shop_name = models.CharField(max_length=100)
    building_no = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.PositiveBigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_details')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, editable=False, default=None, null=True)
    updated_by = models.CharField(max_length=100, editable=False, default=None, null=True)

    def __str__(self):
        return self.shop_name


class ShopProduct(models.Model):
    shop_product_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shop_product')
    shop_details = models.ForeignKey(ShopDetails, on_delete=models.CASCADE, related_name='shop_product')
    offer_percentage = models.FloatField(max_length=5)
    vendor_price = models.FloatField()
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_product')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, editable=False, default=None, null=True)
    updated_by = models.CharField(max_length=100, editable=False, default=None, null=True)

    def __str__(self):
        return f'{self.product} {self.shop_details}'





















# class Category(models.Model):
#     category_id = models.AutoField()
#     category_name = models.CharField(max_length=100)
#     # description = models.TextField(max_length=200)
#
#     class Mobile(Enum):
#         ram = 'ram'
#         internal_memory = 'storage'
#         battery = 'battery'
#         camera = 'camera'
#         os = 'os'
#         display = 'display'
#
#     specifications = JSONField()
#     # if category_name == Mobile:
#     #     for key in Mobile:
#     #         specifications[key] = models.CharField(max_length=100)
#
#     is_active = models.BooleanField(default=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
#     created_by = models.CharField(max_length=100, editable=False, default=None, null=True)
#     updated_by = models.CharField(max_length=100, editable=False, default=None, null=True)
#
#     def __str__(self):
#         return self.category_name
