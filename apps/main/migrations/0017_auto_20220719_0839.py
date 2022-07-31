# Generated by Django 3.1.7 on 2022-07-19 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_auto_20210405_1318'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0016_auto_20210515_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='info',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Information on the application'),
        ),
        migrations.AlterField(
            model_name='application',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.order', verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='application',
            name='sending',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sending', verbose_name='Departure'),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('WAIT', 'Confirmation is expected '), ('CONF', 'Confirmed'), ('DECL', 'Divestable')], default='WAIT', max_length=4, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.country', verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='order',
            name='additional_info',
            field=models.TextField(blank=True, max_length=5000, verbose_name='additional_info'),
        ),
        migrations.AlterField(
            model_name='order',
            name='arrival_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.city', verbose_name='Город получения'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cargo_depth',
            field=models.DecimalField(decimal_places=1, max_digits=10, verbose_name='cargo_depth'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cargo_len',
            field=models.DecimalField(decimal_places=1, max_digits=10, verbose_name='cargo_len'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cargo_type',
            field=models.CharField(choices=[('PACK', 'PACK'), ('BARE', 'BARE')], max_length=4, verbose_name='cargo_type'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cargo_weight',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='cargo_weight'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cargo_width',
            field=models.DecimalField(decimal_places=1, max_digits=10, verbose_name='cargo_width'),
        ),
        migrations.AlterField(
            model_name='order',
            name='departure_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_departure_city', to='main.city', verbose_name='departure city'),
        ),
        migrations.AlterField(
            model_name='order',
            name='departure_date',
            field=models.DateField(verbose_name='departure_date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='direct_deliver',
            field=models.BooleanField(verbose_name='direct_deliver'),
        ),
        migrations.AlterField(
            model_name='order',
            name='direct_deliver_address',
            field=models.CharField(blank=True, max_length=250, verbose_name='direct_deliver_address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='direct_take',
            field=models.BooleanField(verbose_name='direct take?'),
        ),
        migrations.AlterField(
            model_name='order',
            name='direct_take_address',
            field=models.CharField(blank=True, max_length=250, verbose_name='direct_take_address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='insurance_price',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='insurance_price'),
        ),
        migrations.AlterField(
            model_name='order',
            name='recipient_fullname',
            field=models.CharField(max_length=100, verbose_name='recipient fullname'),
        ),
        migrations.AlterField(
            model_name='order',
            name='sender_fullname',
            field=models.CharField(max_length=100, verbose_name='sender fullname'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='arrival_date',
            field=models.DateField(verbose_name='date of receiving'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='arrival_warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sending_arrival_warehouse', to='main.warehouse', verbose_name='Warehouse of receipt'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='company'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='departure_date',
            field=models.DateField(verbose_name='departure date'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='departure_warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sending_departure_warehouse', to='main.warehouse', verbose_name='The warehouse of departure'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='orders',
            field=models.ManyToManyField(blank=True, to='main.Order', verbose_name='orders'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='price_for_m3',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price for the Cubometer'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='total_volume',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='total volume'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='transport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.transport', verbose_name='transport'),
        ),
        migrations.AlterField(
            model_name='transitpoint',
            name='arrival_date',
            field=models.DateField(verbose_name='Arrival date (to this item)'),
        ),
        migrations.AlterField(
            model_name='transitpoint',
            name='arrival_warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.warehouse', verbose_name='Transit warehouse'),
        ),
        migrations.AlterField(
            model_name='transitpoint',
            name='sending',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sending', verbose_name='Departure'),
        ),
        migrations.AlterField(
            model_name='transitpoint',
            name='transport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.transport', verbose_name='Transport (until the next point of the route)'),
        ),
        migrations.AlterField(
            model_name='transport',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='company'),
        ),
        migrations.AlterField(
            model_name='transport',
            name='number',
            field=models.CharField(blank=True, max_length=20, verbose_name='ransport number'),
        ),
        migrations.AlterField(
            model_name='transport',
            name='transport_type',
            field=models.CharField(choices=[('CAR', 'CAR'), ('TRAIN', 'TRAIN'), ('PLANE', 'PLANE'), ('SHIP', 'SHIP')], max_length=5, verbose_name='transport type'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='address',
            field=models.CharField(max_length=250, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.city', verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='company'),
        ),
    ]
