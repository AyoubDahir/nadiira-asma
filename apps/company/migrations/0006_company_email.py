# Generated by Django 3.1.7 on 2021-04-05 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_auto_20210308_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=100),
            preserve_default=False,
        ),
    ]
