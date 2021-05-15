from django.contrib import admin

from apps.main.models import Country, City, Warehouse, Order, Transport, Sending, Application, TransitPoint

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Warehouse)
admin.site.register(Order)
admin.site.register(Transport)
admin.site.register(TransitPoint)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    fields = ('order', 'sending', 'status', 'info', 'price')
    readonly_fields = ('price',)


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    fields = ('company', 'departure_warehouse', 'departure_date', 'arrival_warehouse', 'arrival_date', 'total_volume',
              'transport', 'orders', 'price_for_m3', 'free_volume')
    readonly_fields = ('free_volume',)
