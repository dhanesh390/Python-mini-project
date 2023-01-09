from django.db import models
from django.db.models import JSONField

from user.models import User


# Create your models here.
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
    specification = JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='product_created_user')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='product_updated_user')

    def __str__(self):
        return self.name