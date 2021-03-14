from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import UpdateView

from apps.userprofile.forms import UserForm, ProfileForm
from apps.userprofile.models import Profile


class UpdateUserView(LoginRequiredMixin, UpdateView):
    """
    View for updating user information
    """
    model = User
    form_class = UserForm
    template_name = 'userprofile/form.html'
    login_url = 'login/'
    success_url = '/'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        """
        user can update only his profile
        :param form:
        :return:
        """
        form.save(commit=False)
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    View for updating additional user information
    """
    model = Profile
    form_class = ProfileForm
    template_name = 'userprofile/form.html'
    login_url = 'login/'
    success_url = '/'

    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()

    def form_valid(self, form):
        """
        user can update only his profile
        :param form:
        :return:
        """
        form.save()
        return super().form_valid(form)
