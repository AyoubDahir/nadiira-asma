# Generated by Django 3.1.6 on 2021-02-25 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20210225_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='info',
            field=models.TextField(blank=True, max_length=5000),
        ),
    ]
