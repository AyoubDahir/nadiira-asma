# Generated by Django 3.1.6 on 2021-03-12 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_application_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='sending',
            name='price_for_m3',
            field=models.DecimalField(decimal_places=2, default=100000, max_digits=10, verbose_name='Цена за кубометр'),
            preserve_default=False,
        ),
    ]