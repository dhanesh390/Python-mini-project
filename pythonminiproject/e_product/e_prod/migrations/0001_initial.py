# Generated by Django 4.1.4 on 2023-01-02 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=200)),
                ('specifications', models.TextField(max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default=None, editable=False, max_length=100)),
                ('updated_by', models.CharField(default=None, editable=False, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default=None, editable=False, max_length=100)),
                ('updated_by', models.CharField(default=None, editable=False, max_length=100)),
                ('product_category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='e_prod.category')),
            ],
        ),
        migrations.CreateModel(
            name='ShopDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=100)),
                ('building_no', models.CharField(max_length=100)),
                ('street_name', models.CharField(max_length=100)),
                ('locality', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.PositiveBigIntegerField()),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default=None, editable=False, max_length=100)),
                ('updated_by', models.CharField(default=None, editable=False, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=25)),
                ('user_role', models.CharField(choices=[('admin', 'admin'), ('consumer', 'consumer')], default='consumer', max_length=10)),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default=None, editable=False, max_length=100)),
                ('updated_by', models.CharField(default=None, editable=False, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_price', models.FloatField()),
                ('offer_percentage', models.FloatField(max_length=5)),
                ('vendor_price', models.FloatField()),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='e_prod.product')),
                ('shop_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='e_prod.shopdetails')),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='e_prod.user'),
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='e_prod.user'),
        ),
    ]
