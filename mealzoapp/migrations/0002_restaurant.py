# Generated by Django 5.1.4 on 2024-12-08 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealzoapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('contact_no', models.IntegerField()),
                ('address', models.TextField()),
                ('cuisine_type', models.CharField(max_length=100)),
                ('opening_hours', models.TimeField()),
                ('pan_card', models.FileField(blank=True, null=True, upload_to='pan_cards/')),
                ('restaurant_photo', models.ImageField(blank=True, null=True, upload_to='restaurant_photos/')),
                ('account_number', models.CharField(max_length=20)),
                ('account_name', models.IntegerField()),
                ('ifsc_code', models.CharField(max_length=11)),
                ('branch', models.CharField(max_length=100)),
            ],
        ),
    ]
