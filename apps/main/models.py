from django.contrib.auth.models import User
from django.db import models

from apps.company.models import Company


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.country.name})'


class Warehouse(models.Model):
    address = models.CharField(max_length=250)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.address} ({self.city.name}, {self.city.country.name})'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    departure_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                            related_name='order_departure_warehouse')
    arrival_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='order_arrival_warehouse')

    sender_fullname = models.CharField(max_length=100)
    recipient_fullname = models.CharField(max_length=100)

    direct_take = models.BooleanField()
    direct_take_address = models.CharField(max_length=250, blank=True)

    direct_deliver = models.BooleanField()
    direct_deliver_address = models.CharField(max_length=250, blank=True)

    departure_date = models.DateField()

    CARGO_TYPE_SET = (
        ('PACK', 'Упаковка'),
        ('BARE', 'Без упаковки'),
    )

    cargo_type = models.CharField(max_length=4, choices=CARGO_TYPE_SET)

    cargo_len = models.DecimalField(decimal_places=1, max_digits=10)
    cargo_width = models.DecimalField(decimal_places=1, max_digits=10)
    cargo_depth = models.DecimalField(decimal_places=1, max_digits=10)

    cargo_weight = models.DecimalField(decimal_places=2, max_digits=10)

    insurance_price = models.DecimalField(decimal_places=2, max_digits=15)

    additional_info = models.TextField(max_length=5000, blank=True)

    @property
    def cargo_volume(self):
        return round(self.cargo_len * self.cargo_width * self.cargo_depth, 1) / 1000000

    def __str__(self):
        return f'{self.id}. {self.user.last_name}' \
               f' ({self.departure_warehouse.city} - {self.arrival_warehouse.city})'


class Transport(models.Model):
    TRANSPORT_TYPE_SET = (
        ('CAR', 'Грузовик'),
        ('TRAIN', 'Поезд'),
        ('PLANE', 'Самолёт'),
    )
    transport_type = models.CharField(max_length=5, choices=TRANSPORT_TYPE_SET)
    number = models.CharField(max_length=20, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company}. {self.get_transport_type_display()} ({self.number})'


class Sending(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    departure_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                            related_name='sending_departure_warehouse')
    departure_date = models.DateField()

    arrival_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='sending_arrival_warehouse')

    arrival_date = models.DateField()

    total_volume = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Общий объём в м^3')
    occupied_volume = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                          verbose_name='Занятый объём в м^3')

    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)

    orders = models.ManyToManyField(Order, blank=True)

    @property
    def free_volume(self):
        return round(self.total_volume - self.occupied_volume, 2)

    def __str__(self):
        return f'{self.company}. {self.departure_warehouse} -> {self.arrival_warehouse}.' \
               f' {self.departure_date}-{self.arrival_date} '


class Application(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sending = models.ForeignKey(Sending, on_delete=models.CASCADE)

    STATUS_SET = (
        ('WAIT', 'Ожидается подтверждение'),
        ('CONF', 'Подтверждено'),

    )
    status = models.CharField(max_length=4, choices=STATUS_SET, default='WAIT')

    def __str__(self):
        return f'{self.get_status_display()}. {self.order}. {self.sending}'
