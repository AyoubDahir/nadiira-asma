from django import forms

from apps.company.models import WorkerProfile
from apps.main.models import Warehouse


class WorkerProfileForm(forms.ModelForm):
    class Meta:
        model = WorkerProfile
        fields = ('user', 'position')


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ('address', 'city')
