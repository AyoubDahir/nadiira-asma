from django.urls import path

from apps.userprofile.views import UpdateUserView, UpdateProfileView

app_name = 'userprofile'
urlpatterns = [
    path('', UpdateUserView.as_view(), name='profile'),
    path('info/', UpdateProfileView.as_view(), name='info'),
]
