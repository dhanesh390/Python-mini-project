from django.db import models


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=25)
    ADMIN = 'admin'
    CONSUMER = 'consumer'
    USER_ROLES = [
        (ADMIN, 'admin'),
        (CONSUMER, 'consumer')
    ]
    user_role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default=CONSUMER,
    )
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, editable=False, default=None, null=True)
    updated_by = models.CharField(max_length=100, editable=False, default=None, null=True)

    def __str__(self):
        return self.user_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    specifications = models.TextField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, editable=False, default=None, null=True)
    updated_by = models.CharField(max_length=100, editable=False, default=None, null=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    product_category = models.OneToOneField(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, editable=False, default=None, null=True)
    updated_by = models.CharField(max_length=100, editable=False, default=None, null=True)

    def __str__(self):
        return self.product_name


class ShopDetails(models.Model):
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shop_product')
    shop_details = models.ForeignKey(ShopDetails, on_delete=models.CASCADE, related_name='shop')
    actual_price = models.FloatField()
    offer_percentage = models.FloatField(max_length=5)
    vendor_price = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, editable=False, default=None, null=True)
    updated_by = models.CharField(max_length=100, editable=False, default=None, null=True)

    def __str__(self):
        return f'{self.product} {self.shop_details}'


