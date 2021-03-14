from django import forms
from django.contrib.auth.models import User

from apps.userprofile.models import Profile


class UserForm(forms.ModelForm):
    """
    Form for account information
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    """
    Form for additional account information
    """
    class Meta:
        model = Profile
        fields = ('phone', )
