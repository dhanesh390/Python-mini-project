# Generated by Django 4.1.5 on 2023-01-05 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_product_comparison', '0002_alter_user_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopdetail',
            old_name='phone',
            new_name='contact_number',
        ),
        migrations.RenameField(
            model_name='shopdetail',
            old_name='shop_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='user',
            name='contact_number',
            field=models.CharField(max_length=15),
        ),
    ]