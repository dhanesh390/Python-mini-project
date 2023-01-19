from django.db import models


# Create your models here.
class User(models.Model):
    """ This class contains the attributes of the user object"""
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

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
