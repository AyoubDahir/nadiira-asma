from django import forms

from apps.company.models import WorkerProfile
from apps.main.models import Warehouse, Transport, Sending


class WorkerProfileForm(forms.ModelForm):
    class Meta:
        model = WorkerProfile
        fields = ('user', 'position')


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ('address', 'city')


class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = ('transport_type', 'number')


class SendingForm(forms.ModelForm):
    class Meta:
        model = Sending
        fields = ('departure_warehouse', 'arrival_warehouse', 'total_volume', 'occupied_volume', 'transport')
