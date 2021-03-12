from django import forms

from apps.company.models import WorkerProfile
from apps.main.models import Warehouse, Transport, Sending, Application


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
        fields = (
            'departure_warehouse', 'departure_date', 'arrival_warehouse', 'arrival_date', 'total_volume', 'transport')


class ApplicationManageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApplicationManageForm, self).__init__(*args, **kwargs)
        self.fields['order'].disabled = True
        self.fields['sending'].disabled = True

    class Meta:
        model = Application
        fields = ('order', 'sending', 'status', 'info')
