import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

from apps.main.forms import OrderForm, ApplicationForm
from apps.main.models import Order, Sending, Application


class MainPageView(TemplateView):
    """
    View for main page of site
    """
    template_name = 'main/index.html'


class OrderList(LoginRequiredMixin, ListView):
    """
    View for list of all orders, created by user
    """
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
        """
        :param kwargs:
        :return: context, with sendings appropriate for order
        """
        context = super().get_context_data(**kwargs)
        try:
            application = Application.objects.get(order=self.object)
        except Exception:
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
        else:
            context['application'] = application
        return context


class CreateApplication(LoginRequiredMixin, CreateView):
    """
    View for creation of application
    (for users)
    """
    model = Application
    template_name = 'main/forms/create_application_form.html'
    form_class = ApplicationForm
    login_url = 'login/'
    success_url = reverse_lazy('main:applications')

    def form_valid(self, form):
        """
        Substitution of selected order and sending
        :param form:
        :return:
        """
        form.instance.order = Order.objects.get(pk=self.kwargs['order_pk'])
        form.instance.sending = Sending.objects.get(pk=self.kwargs['sending_pk'])
        if self.request.user == form.instance.order.user:
            return super().form_valid(form)
        else:
            raise Http404('You can not do it')


class ApplicationList(LoginRequiredMixin, ListView):
    """
    View for list all applications
    (for users)
    """
    model = Application

    template_name = 'main/applications.html'

    def get_queryset(self):
        """
        Show only orders of user
        :return:
        """
        try:
            queryset = Application.objects.filter(order__user=self.request.user)
        except Exception:
            raise Http404
        else:
            return queryset


class DeleteApplication(LoginRequiredMixin, DeleteView):
    """
    View for deleting application
    (for users)
    """
    model = Application
    template_name = 'main/forms/delete_application_form.html'
    success_url = reverse_lazy('main:orders')

    def delete(self, request, *args, **kwargs):
        """
        on delete of application order deletes from sending
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.object = self.get_object()
        if self.object.status == 'CONF':
            order = self.object.order
            sending = self.object.sending
            sending.orders.remove(order)
            sending.save()
        return super(DeleteApplication, self).delete(request, *args, **kwargs)
