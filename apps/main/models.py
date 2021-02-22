from django.contrib.auth.models import User
from django.db import models


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

    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.address} ({self.city.name}, {self.city.country.name})'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    departure_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    arrival_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

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

    cargo_type = models.CharField(max_length=1, choices=CARGO_TYPE_SET)

    cargo_len = models.DecimalField(decimal_places=2)
    cargo_width = models.DecimalField(decimal_places=2)
    cargo_depth = models.DecimalField(decimal_places=2)

    cargo_weight = models.DecimalField(decimal_places=2)

    insurance_price = models.DecimalField(decimal_places=2)

    additional_info = models.TextField(max_length=5000, blank=True)

    @property
    def cargo_volume(self):
        return round(self.cargo_len * self.cargo_width * self.cargo_depth, 2)

    def __str__(self):
        return f'{self.id}. {self.user.last_name}' \
               f' ({self.departure_warehouse.city} - {self.arrival_warehouse.city})'


