from jsonfield import JSONField
from django.db import models


# Create your models here.
class User(models.Model):
    """ This class contains the attributes of the user object"""
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, error_messages={'first_name': 'field should only contain alphabets'})
    last_name = models.CharField(max_length=100, error_messages={'last_name': 'field should only contain alphabets'})
    username = models.CharField(max_length=100, unique=True,
                                error_messages={'first_name': 'Username already exists'})
    password = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

    class Role(models.TextChoices):
        """ This class is implemented to have choices of roles for the user"""
        consumer = 'consumer',
        admin = 'admin'

    user_role = models.TextField(choices=Role.choices, default='consumer')
    is_active = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.OneToOneField('self', on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='created_user')
    updated_by = models.OneToOneField('self', on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='updated_user')

    def __str__(self):
        return self.first_name


class Product(models.Model):
    """ This class contains the attributes of the product object"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200)

    class Category(models.TextChoices):
        """ This class is implemented to provide the choices of product categories for product object"""
        mobile = 'mobile'
        laptop = 'laptop'
        tv = 'tv'

    category_type = models.TextField(choices=Category.choices, default='Null')
    specification = JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='product_created_user')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='product_updated_user')

    def __str__(self):
        return self.name


class ShopDetail(models.Model):
    """ This class contain the attributes for the shop details object"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10)
    building_no = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_details')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='shop_created_user')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='shop_updated_user')

    def __str__(self):
        return self.name


class ShopProduct(models.Model):
    """ this class is implemented to maintain the relationship between various product and various shops"""
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shop_product')
    shop_detail = models.ForeignKey(ShopDetail, on_delete=models.CASCADE, related_name='shop_product')
    actual_price = models.FloatField(default=0)
    offer_percentage = models.FloatField(max_length=5)
    vendor_price = models.FloatField()
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_product')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='shop_product_created_user')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='shop_product_updated_user')

    def __str__(self):
        return f'{self.product} {self.id}'

