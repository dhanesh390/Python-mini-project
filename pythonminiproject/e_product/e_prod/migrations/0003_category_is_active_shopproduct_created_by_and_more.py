# Generated by Django 4.1.4 on 2023-01-02 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_prod', '0002_alter_product_product_name_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='created_by',
            field=models.CharField(default=None, editable=False, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='updated_by',
            field=models.CharField(default=None, editable=False, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='created_by',
            field=models.CharField(default=None, editable=False, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_by',
            field=models.CharField(default=None, editable=False, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_by',
            field=models.CharField(default=None, editable=False, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_by',
            field=models.CharField(default=None, editable=False, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shopdetails',
            name='created_by',
            field=models.CharField(default=None, editable=False, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shopdetails',
            name='updated_by',
            field=models.CharField(default=None, editable=False, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_by',
            field=models.CharField(default=None, editable=False, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_by',
            field=models.CharField(default=None, editable=False, max_length=100, null=True),
        ),
    ]
