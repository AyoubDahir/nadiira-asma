from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from apps.company.forms import WorkerProfileForm, WarehouseForm
from apps.company.models import WorkerProfile, Company
from apps.main.models import Warehouse


class CompanyList(ListView):
    """
    View for list all transport companies
    """
    model = Company
    template_name = 'company/index.html'


class CompanyDetail(DetailView):
    """
    View for details of transport company
    """
    model = Company
    template_name = 'company/detail.html'


class CreateWorkerProfile(LoginRequiredMixin, CreateView):
    """
    View for creation of transport company worker
    (only users with owner accounts can make this)
    """
    model = WorkerProfile
    template_name = 'company/forms/create_form.html'
    form_class = WorkerProfileForm
    login_url = 'login/'
    success_url = reverse_lazy('company:listworkers')

    def form_valid(self, form):
        """
        Set company of worker same as company of creator
        :param form:
        :return:
        """
        form.instance.company = Company.objects.get(name=WorkerProfile.objects.get(user=self.request.user).company)
        return super().form_valid(form)


class UpdateWorkerProfile(LoginRequiredMixin, UpdateView):
    """
    View for updating of transport company worker
    (only users with owner accounts can make this)
    """
    model = WorkerProfile
    template_name = 'company/forms/update_form.html'
    form_class = WorkerProfileForm
    login_url = 'login/'
    success_url = reverse_lazy('company:listworkers')

    def form_valid(self, form):
        """
        Set company of worker same as company of creator
        :param form:
        :return:
        """
        form.instance.company = Company.objects.get(name=WorkerProfile.objects.get(user=self.request.user).company)
        return super().form_valid(form)


class DeleteWorkerProfile(LoginRequiredMixin, DeleteView):
    """
    View for updating of transport company worker
    (only users with owner accounts can make this)
    """
    model = WorkerProfile
    template_name = 'company/forms/delete_form.html'
    success_url = reverse_lazy('company:listworkers')


class WorkerProfileList(LoginRequiredMixin, ListView):
    """
    View for list all companies workers
    """
    model = WorkerProfile
    template_name = 'company/workers.html'

    def get_queryset(self):
        """
        Show only workers of companies same as company of creator
        :return:
        """
        try:
            queryset = WorkerProfile.objects.filter(
                company=Company.objects.get(name=WorkerProfile.objects.get(user=self.request.user).company.name))
        except Exception:
            raise Http404
        else:
            return queryset


class CompanyManagement(LoginRequiredMixin, TemplateView):
    template_name = 'company/manage.html'


class WarehouseList(LoginRequiredMixin, ListView):
    """
    View for list all companies warehouses
    """
    model = Warehouse
    template_name = 'company/warehouses.html'

    def get_queryset(self):
        """
        Show only workers of companies same as company of creator
        :return:
        """
        try:
            queryset = Warehouse.objects.filter(
                company=Company.objects.get(name=WorkerProfile.objects.get(user=self.request.user).company.name))
        except Exception:
            raise Http404
        else:
            return queryset


class CreateWarehouse(LoginRequiredMixin, CreateView):
    """
    View for creation of transport company worker
    (only users with owner accounts can make this)
    """
    model = Warehouse
    template_name = 'company/forms/create_form.html'
    form_class = WarehouseForm
    login_url = 'login/'
    success_url = reverse_lazy('company:listwarehouse')

    def form_valid(self, form):
        """
        Set company of worker same as company of creator
        :param form:
        :return:
        """
        form.instance.company = Company.objects.get(name=WorkerProfile.objects.get(user=self.request.user).company)
        return super().form_valid(form)


class UpdateWarehouse(LoginRequiredMixin, UpdateView):
    """
    View for updating of transport company worker
    (only users with owner accounts can make this)
    """
    model = Warehouse
    template_name = 'company/forms/update_form.html'
    form_class = WarehouseForm
    login_url = 'login/'
    success_url = reverse_lazy('company:listwarehouse')

    def form_valid(self, form):
        """
        Set company of worker same as company of creator
        :param form:
        :return:
        """
        form.instance.company = Company.objects.get(name=WorkerProfile.objects.get(user=self.request.user).company)
        return super().form_valid(form)


class DeleteWarehouse(LoginRequiredMixin, DeleteView):
    """
    View for updating of transport company worker
    (only users with owner accounts can make this)
    """
    model = Warehouse
    template_name = 'company/forms/delete_warehouse_form.html'
    success_url = reverse_lazy('company:listwarehouse')
