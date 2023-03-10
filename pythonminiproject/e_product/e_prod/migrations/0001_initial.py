# Generated by Django 4.1.4 on 2023-01-03 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=100, unique=True)),
                ('product_price', models.FloatField(default=0)),
                ('product_description', models.TextField(max_length=200)),
                ('product_category_type', models.TextField(choices=[('mobile', 'Mobile'), ('laptop', 'Laptop'), ('tv', 'Tv')], default='Null')),
                ('ram', models.CharField(max_length=100, null=True)),
                ('battery', models.CharField(max_length=100, null=True)),
                ('internal_storage', models.CharField(max_length=100, null=True)),
                ('front_camera', models.CharField(max_length=100, null=True)),
                ('external_storage', models.CharField(max_length=100, null=True)),
                ('back_camera', models.CharField(max_length=100, null=True)),
                ('cpu', models.CharField(max_length=100, null=True)),
                ('gpu', models.CharField(max_length=100, null=True)),
                ('display', models.CharField(max_length=100, null=True)),
                ('screen_size', models.CharField(max_length=100, null=True)),
                ('screen_resolution', models.CharField(max_length=100, null=True)),
                ('no_of_speakers', models.CharField(max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default=None, editable=False, max_length=100, null=True)),
                ('updated_by', models.CharField(default=None, editable=False, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShopDetails',
            fields=[
                ('shop_id', models.AutoField(primary_key=True, serialize=False)),
                ('shop_name', models.CharField(max_length=100)),
                ('building_no', models.CharField(max_length=100)),
                ('street_name', models.CharField(max_length=100)),
                ('locality', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.PositiveBigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default=None, editable=False, max_length=100, null=True)),
                ('updated_by', models.CharField(default=None, editable=False, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=25)),
                ('user_role', models.TextField(choices=[('consumer', 'Consumer'), ('admin', 'Admin')], default='consumer')),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default=None, editable=False, max_length=100, null=True)),
                ('updated_by', models.CharField(default=None, editable=False, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('shop_product_id', models.AutoField(primary_key=True, serialize=False)),
                ('offer_percentage', models.FloatField(max_length=5)),
                ('vendor_price', models.FloatField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default=None, editable=False, max_length=100, null=True)),
                ('updated_by', models.CharField(default=None, editable=False, max_length=100, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_product', to='e_prod.product')),
                ('shop_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_product', to='e_prod.shopdetails')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_product', to='e_prod.user')),
            ],
        ),
        migrations.AddField(
            model_name='shopdetails',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_details', to='e_prod.user'),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='e_prod.user'),
        ),
    ]
