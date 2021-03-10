from django.contrib.auth.models import User
from django.db import models

from apps.company.models import Company


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')

    def __str__(self):
        return f'{self.name} ({self.country.name})'


class Warehouse(models.Model):
    address = models.CharField(max_length=250, verbose_name='Адрес')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')

    def __str__(self):
        return f'{self.address} ({self.city.name}, {self.city.country.name})'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    departure_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                            related_name='order_departure_warehouse', verbose_name='Склад отправления')
    arrival_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='order_arrival_warehouse',
                                          verbose_name='Склад получения')

    sender_fullname = models.CharField(max_length=100, verbose_name='ФИО отправителя')
    recipient_fullname = models.CharField(max_length=100, verbose_name='ФИО получателя')

    direct_take = models.BooleanField(verbose_name='Нужно ли забрать от отправителя?')
    direct_take_address = models.CharField(max_length=250, blank=True, verbose_name='Адрес отправителя')

    direct_deliver = models.BooleanField(verbose_name='Нужно ли доставить получателю?')
    direct_deliver_address = models.CharField(max_length=250, blank=True, verbose_name='Адрес получателя')

    departure_date = models.DateField(verbose_name='Дата отправления')

    CARGO_TYPE_SET = (
        ('PACK', 'Упаковка'),
        ('BARE', 'Без упаковки'),
    )

    cargo_type = models.CharField(max_length=4, choices=CARGO_TYPE_SET, verbose_name='Тип груза')

    cargo_len = models.DecimalField(decimal_places=1, max_digits=10, verbose_name='Длина груза (см)')
    cargo_width = models.DecimalField(decimal_places=1, max_digits=10, verbose_name='Ширина груза (см)')
    cargo_depth = models.DecimalField(decimal_places=1, max_digits=10, verbose_name='Глубина груза (см)')

    cargo_weight = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Вес груза (кг)')

    insurance_price = models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Стоимость страховки (руб)')

    additional_info = models.TextField(max_length=5000, blank=True, verbose_name='Дополнительная информация')

    @property
    def cargo_volume(self):
        return round(self.cargo_len * self.cargo_width * self.cargo_depth, 1) / 1000000

    def __str__(self):
        return f'Заказ №{self.id}. {self.user.last_name}' \
               f' ({self.departure_warehouse.city} - {self.arrival_warehouse.city}). {self.departure_date}'

    cargo_volume.fget.short_description = 'Объём груза (м^3)'


class Transport(models.Model):
    TRANSPORT_TYPE_SET = (
        ('CAR', 'Грузовик'),
        ('TRAIN', 'Поезд'),
        ('PLANE', 'Самолёт'),
    )
    transport_type = models.CharField(max_length=5, choices=TRANSPORT_TYPE_SET, verbose_name='Тип транспорта')
    number = models.CharField(max_length=20, blank=True, verbose_name='Номер транспорта')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')

    def __str__(self):
        return f'{self.company}. {self.get_transport_type_display()} ({self.number})'


class Sending(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')

    departure_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                            related_name='sending_departure_warehouse',
                                            verbose_name='Склад отправления')
    departure_date = models.DateField(verbose_name='Дата отправления')

    arrival_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='sending_arrival_warehouse',
                                          verbose_name='Склад получения')

    arrival_date = models.DateField(verbose_name='Дата получения')

    total_volume = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Общий объём в м^3')
    occupied_volume = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                          verbose_name='Занятый объём в м^3')

    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, verbose_name='Транспорт')

    orders = models.ManyToManyField(Order, blank=True, verbose_name='Заказы')

    @property
    def free_volume(self):
        return round(self.total_volume - self.occupied_volume, 2)

    def __str__(self):
        return f'Отправление №{self.id}. {self.company}. {self.departure_warehouse} -> {self.arrival_warehouse}.' \
               f' {self.departure_date}-{self.arrival_date} '

    free_volume.fget.short_description = 'Свободное место (м^3)'


class Application(models.Model):
    order = models.OneToOneField(to=Order, on_delete=models.CASCADE, verbose_name='Заказ')
    sending = models.ForeignKey(Sending, on_delete=models.CASCADE, verbose_name='Отправление')

    STATUS_SET = (
        ('WAIT', 'Ожидается подтверждение'),
        ('CONF', 'Подтверждено'),
        ('DECL', 'Отклонено'),

    )
    status = models.CharField(max_length=4, choices=STATUS_SET, default='WAIT', verbose_name='Статус')
    info = models.CharField(max_length=1000, blank=True, verbose_name='Информация по заявке')

    def __str__(self):
        return f'{self.get_status_display()}. {self.order}. {self.sending}'
