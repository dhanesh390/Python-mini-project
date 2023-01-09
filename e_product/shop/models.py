from django.db import models

from user.models import User


# Create your models here.
class Shop(models.Model):
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='shop_created_user')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='shop_updated_user')

    def __str__(self):
        return self.name
