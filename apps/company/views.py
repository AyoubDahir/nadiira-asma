from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from apps.company.forms import WorkerProfileForm
from apps.company.models import WorkerProfile, Company


class CreateWorkerProfile(LoginRequiredMixin, CreateView):
    model = WorkerProfile
    template_name = 'company/form.html'
    form_class = WorkerProfileForm
    login_url = 'login/'
    success_url = '/'

    def form_valid(self, form):
        form.instance.company = Company.objects.get(name=WorkerProfile.objects.get(user=self.request.user).company)
        return super().form_valid(form)
