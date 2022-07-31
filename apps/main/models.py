from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from CargoDelivery import settings
from apps.company.models import Company, WorkerProfile
from apps.main.tasks import send_email_celery, send_many_email_celery


class Country(models.Model):
    """
    Model of country
    """
    name = models.CharField(max_length=100, verbose_name='Name')

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Model of city in country
    """
    name = models.CharField(max_length=100, verbose_name='name')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='country')

    def __str__(self):
        return f'{self.name} ({self.country.name})'


class Warehouse(models.Model):
    """
    Model of warehouse in city
    """
    address = models.CharField(max_length=250, verbose_name='address')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='company')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='city')

    def __str__(self):
        return f'{self.address} ({self.city.name}, {self.city.country.name})'


class Order(models.Model):
    """
    Model of order
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')

    departure_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                       related_name='order_departure_city', verbose_name='departure city')
    arrival_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                     verbose_name='arrival_city')

    sender_fullname = models.CharField(max_length=100, verbose_name='sender fullname')
    recipient_fullname = models.CharField(max_length=100, verbose_name='recipient fullname')

    direct_take = models.BooleanField(verbose_name='direct take?')
    direct_take_address = models.CharField(max_length=250, blank=True, verbose_name='direct_take_address')

    direct_deliver = models.BooleanField(verbose_name='direct_deliver')
    direct_deliver_address = models.CharField(max_length=250, blank=True, verbose_name='direct_deliver_address')

    departure_date = models.DateField(verbose_name='departure_date')

    CARGO_TYPE_SET = (
        ('PACK', 'PACK'),
        ('BARE', 'BARE'),
    )

    cargo_type = models.CharField(max_length=4, choices=CARGO_TYPE_SET, verbose_name='cargo_type')

    cargo_len = models.DecimalField(decimal_places=1, max_digits=10, verbose_name='cargo_len')
    cargo_width = models.DecimalField(decimal_places=1, max_digits=10, verbose_name='cargo_width')
    cargo_depth = models.DecimalField(decimal_places=1, max_digits=10, verbose_name='cargo_depth')

    cargo_weight = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='cargo_weight')

    insurance_price = models.DecimalField(decimal_places=2, max_digits=15, verbose_name='insurance_price')

    additional_info = models.TextField(max_length=5000, blank=True, verbose_name='additional_info')

    @property
    def cargo_volume(self):
        """
        :return: volume of cargo in m^3
        """
        return round(self.cargo_len * self.cargo_width * self.cargo_depth, 2) / 1000000

    def __str__(self):
        return f'Заказ №{self.id}. ({self.sender_fullname}.' \
               f' {self.departure_city} -> {self.arrival_city}. {self.recipient_fullname}) . {self.departure_date}'

    cargo_volume.fget.short_description = 'cargo_volume'


class Transport(models.Model):
    """
    Model of transport
    """
    TRANSPORT_TYPE_SET = (
        ('CAR', 'CAR'),
        ('TRAIN', 'TRAIN'),
        ('PLANE', 'PLANE'),
        ('SHIP', 'SHIP'),
    )
    transport_type = models.CharField(max_length=5, choices=TRANSPORT_TYPE_SET, verbose_name='transport type')
    number = models.CharField(max_length=20, blank=True, verbose_name='ransport number')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='company')

    def __str__(self):
        return f'{self.company}. {self.get_transport_type_display()} ({self.number})'


class Sending(models.Model):
    """
    Model of sending
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='company')

    departure_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                            related_name='sending_departure_warehouse',
                                            verbose_name='The warehouse of departure')
    departure_date = models.DateField(verbose_name='departure date')

    arrival_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='sending_arrival_warehouse',
                                          verbose_name='Warehouse of receipt')

    arrival_date = models.DateField(verbose_name='date of receiving')

    total_volume = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='total volume')

    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, verbose_name='transport')

    orders = models.ManyToManyField(Order, blank=True, verbose_name='orders')

    price_for_m3 = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price for the Cubometer')

    @property
    def free_volume(self):
        """
        :return: difference between total volume and sum of all orders volume in m^3
        """
        summ = sum([order.cargo_volume for order in self.orders.all()])
        return self.total_volume - round(summ, 2)

    @property
    def days(self):
        """
        Calculate number of days between departure and arrival
        """
        days_list = ['day', 'days']
        num_days = (self.arrival_date - self.departure_date).days
        if num_days % 10 == 1 and num_days % 100 != 11:
            p = 0
        elif 2 <= num_days % 10 <= 4 and (num_days % 100 < 10 or num_days % 100 >= 20):
            p = 1
        else:
            p = 2
        return f'{num_days} {days_list[p]}'

    def __str__(self):
        return f'Departure No.{self.id}. {self.company}. {self.departure_warehouse} -> {self.arrival_warehouse}.' \
               f' {self.departure_date} -> {self.arrival_date} '

    free_volume.fget.short_description = 'Departure No. Switching Place (m^3)'


class Application(models.Model):
    """
    Model of order application
    """
    order = models.OneToOneField(to=Order, on_delete=models.CASCADE, verbose_name='order')
    sending = models.ForeignKey(Sending, on_delete=models.CASCADE, verbose_name='Departure')

    STATUS_SET = (
        ('WAIT', 'Confirmation is expected '),
        ('CONF', 'Confirmed'),
        ('DECL', 'Divestable'),

    )
    status = models.CharField(max_length=4, choices=STATUS_SET, default='WAIT', verbose_name='status')

    info = models.CharField(max_length=1000, blank=True, verbose_name='Information on the application')

    @property
    def price(self):
        """
        :return: calculated price, according to order volume and price of sending
        """
        return round(float(self.order.cargo_volume) * float(self.sending.price_for_m3), 2)

    def __str__(self):
        return f'{self.get_status_display()}. {self.order}. {self.sending}'


class TransitPoint(models.Model):
    sending = models.ForeignKey(Sending, on_delete=models.CASCADE,
                                verbose_name='Departure')
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE,
                                  verbose_name='Transport (until the next point of the route)')
    arrival_date = models.DateField(verbose_name='Arrival date (to this item)')

    arrival_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                     verbose_name='Transit warehouse')

    def __str__(self):
        return f'Transit point {self.sending}, {self.transport}, {self.arrival_date}, {self.arrival_warehouse}'


@receiver(post_save, sender=Sending)
def new_sendings_email(sender, instance, created, **kwargs):
    """
    Signal for sending emails with new sendings (for users)
    """
    if created:

        for order in Order.objects.filter(departure_city=instance.departure_warehouse.city,
                                          arrival_city=instance.arrival_warehouse.city,
                                          departure_date=instance.departure_date):

            need_send = False
            try:
                # Check for application doesn't exists
                if order.application:
                    pass
            except ObjectDoesNotExist:
                need_send = True
            else:
                # Check for application doesn't confirmed
                if order.application.status != 'CONF':
                    need_send = True

            if need_send:
                user_email = order.user.email
                subject = 'A new departure is available for your order'
                html_message = render_to_string('emails/new_sending.html',
                                                {'order': order, 'sending': instance, 'SITE_URL': settings.SITE_URL})
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL
                send_email_celery.delay(subject, plain_message, from_email, user_email, html_message)


@receiver(post_save, sender=Application)
def application_status_email(sender, instance, created, **kwargs):
    """
    Signal for sending emails when manager change its status (for users)
    """
    status = ''
    if instance.status == 'CONF':
        status = 'Confirmed'
    elif instance.status == 'DECL':
        status = 'Divestable'

    if status:
        user_email = instance.order.user.email
        order = Order.objects.get(application=instance)
        sending = Sending.objects.get(application=instance)
        subject = 'subject'
        html_message = render_to_string('emails/application_status.html',
                                        {'status': status, 'order': order, 'sending': sending,
                                         'SITE_URL': settings.SITE_URL})
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        send_email_celery.delay(subject, plain_message, from_email, user_email, html_message)


@receiver(post_save, sender=Application)
def application_created_email(sender, instance, created, **kwargs):
    """
    Signal for sending emails when new application created (for workers)
    """
    if created:
        emails = []
        workers_list = WorkerProfile.objects.filter(company__sending__application=instance)
        for worker in workers_list:
            emails.append(worker.user.email)

        order = Order.objects.get(application=instance)
        sending = Sending.objects.get(application=instance)
        subject = 'Появилась новая заявка для вашей компании'
        html_message = render_to_string('emails/application_created.html',
                                        {'order': order, 'sending': sending, 'application': instance,
                                         'SITE_URL': settings.SITE_URL})
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        send_many_email_celery.delay(subject, plain_message, from_email, emails, html_message)
