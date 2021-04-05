from django import forms

from apps.main.models import Order, Application


class OrderForm(forms.ModelForm):
    """
    Form for order of user
    """

    class Meta:
        model = Order
        fields = ('departure_city', 'arrival_city', 'sender_fullname', 'recipient_fullname',
                  'direct_take', 'direct_take_address', 'direct_deliver', 'direct_deliver_address',
                  'departure_date', 'cargo_type', 'cargo_len', 'cargo_width', 'cargo_depth', 'cargo_weight',
                  'insurance_price', 'additional_info')


class OrderCreationForm(forms.ModelForm):
    """
    Form for order of user
    """

    def __init__(self, *args, **kwargs):
        if user := kwargs.pop('user'):
            super(OrderCreationForm, self).__init__(*args, **kwargs)
            print(user)
            self.fields['sender_fullname'].initial = user.last_name + ' ' + user.first_name

    class Meta:
        model = Order
        fields = ('departure_city', 'arrival_city', 'sender_fullname', 'recipient_fullname',
                  'direct_take', 'direct_take_address', 'direct_deliver', 'direct_deliver_address',
                  'departure_date', 'cargo_type', 'cargo_len', 'cargo_width', 'cargo_depth', 'cargo_weight',
                  'insurance_price', 'additional_info')


class ApplicationForm(forms.ModelForm):
    """"
    Form for application of user order.
    Only confirmation, fields are prepopulated and not shown
    """

    class Meta:
        model = Application
        fields = ()
