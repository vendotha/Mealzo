# Generated by Django 5.1.4 on 2024-12-10 18:33

import django.db.models.deletion
import mealzoapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealzoapp', '0006_income_inventoryitem_menuitem_order_orderitem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer_email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Preparing', 'Preparing'), ('Ready', 'Ready for Delivery'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='menu_item',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='mealzoapp.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='restaurant_photo',
            field=models.ImageField(blank=True, null=True, upload_to=mealzoapp.models.restaurant_photo_upload_to),
        ),
    ]
