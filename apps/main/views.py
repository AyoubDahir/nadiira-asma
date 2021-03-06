import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

from apps.main.forms import OrderForm
from apps.main.models import Order, Sending


class MainPageView(TemplateView):
    template_name = 'main/index.html'


class OrderList(ListView):
    model = Order

    template_name = 'main/orders.html'

    def get_queryset(self):
        """
        Show only orders of user
        :return:
        """
        try:
            queryset = Order.objects.filter(user=self.request.user)
        except Exception:
            raise Http404
        else:
            return queryset


class CreateOrder(LoginRequiredMixin, CreateView):
    """
    View for creation of order
    (for users)
    """
    model = Order
    template_name = 'main/forms/create_form.html'
    form_class = OrderForm
    login_url = 'login/'
    success_url = reverse_lazy('main:orders')

    def form_valid(self, form):
        """
        Set user as request.user
        :param form:
        :return:
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateOrder(LoginRequiredMixin, UpdateView):
    """
    View for updating of order
    (for users)
    """
    model = Order
    template_name = 'main/forms/update_form.html'
    form_class = OrderForm
    login_url = 'login/'
    success_url = reverse_lazy('main:orders')

    def form_valid(self, form):
        """
        Set user as request.user
        :param form:
        :return:
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteOrder(LoginRequiredMixin, DeleteView):
    """
    View for deleting orders
    (for users)
    """
    model = Order
    template_name = 'main/forms/delete_form.html'
    success_url = reverse_lazy('main:orders')


class OrderSendings(LoginRequiredMixin, DetailView):
    """
    View for matching sendings for order
    """
    model = Order

    template_name = 'main/order_sendings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        matching_sendings = Sending.objects.all().filter(departure_warehouse=self.object.departure_warehouse,
                                                         arrival_warehouse=self.object.arrival_warehouse,
                                                         departure_date=self.object.departure_date)

        near_matching_sendings = Sending.objects.all().filter(departure_warehouse=self.object.departure_warehouse,
                                                              arrival_warehouse=self.object.arrival_warehouse,
                                                              departure_date__gte=self.object.departure_date - datetime.timedelta(
                                                                  days=7),
                                                              departure_date__lte=self.object.departure_date + datetime.timedelta(
                                                                  days=7)).difference(matching_sendings)

        context['sendings'] = matching_sendings
        context['near_sendings'] = near_matching_sendings
        return context
