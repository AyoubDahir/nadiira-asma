from django import forms
from django.contrib.auth.models import User

from apps.userprofile.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', )
