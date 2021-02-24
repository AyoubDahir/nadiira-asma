from django.contrib import admin

from apps.main.models import Country, City, Warehouse, Order, Transport, Sending, Application

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Warehouse)
admin.site.register(Order)
admin.site.register(Transport)
admin.site.register(Sending)
admin.site.register(Application)
