# Generated by Django 3.1.6 on 2021-03-12 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_sending_price_for_m3'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sending',
            name='occupied_volume',
        ),
    ]