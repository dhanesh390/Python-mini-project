from django.db import models


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=25)
    ADMIN = 'ad'
    CONSUMER = 'con'
    USER_ROLES = [
        (ADMIN, 'admin'),
        (CONSUMER, 'consumer')
    ]
    user_role = models.CharField(
        max_length=3,
        choices=USER_ROLES,
        default=CONSUMER,
    )
    is_active = True
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, editable=False, default=None)
    updated_by = models.CharField(max_length=100, editable=False, default=None)

    def __repr__(self):
        return self.user_name

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.created_by = self.user_name
        self.updated_by = self.user_name
        super().save(self)


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    specifications = models.TextField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, editable=False, default=None)
    updated_by = models.CharField(max_length=100, editable=False, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category')

    def __repr__(self):
        return self.category_name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.created_by = self.user
        self.updated_by = self.user
        super().save(self)


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_category = models.OneToOneField
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product')
    # shop_details = models.ManyToManyField(ShopDetails, related_name='product')
    product_is_available = True
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, editable=False, default=None)
    updated_by = models.CharField(max_length=100, editable=False, default=None)

    def __repr__(self):
        return self.product_name

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.created_by = self.user
        self.updated_by = self.user
        super().save(self)


class ShopDetails(models.Model):
    shop_name = models.CharField(max_length=100)
    building_no = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.PositiveBigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_details')
    products = models.ManyToManyField(Product, related_name='shop_details')
    is_active = True
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, editable=False, default=None)
    updated_by = models.CharField(max_length=100, editable=False, default=None)

    def __repr__(self):
        return self.shop_name

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.created_by = self.user
        self.updated_by = self.user
        super().save(self)
