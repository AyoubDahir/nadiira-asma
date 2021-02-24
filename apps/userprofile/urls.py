from django.urls import path

from apps.userprofile.views import UpdateUserView, UpdateProfileView

app_name = 'userprofile'
urlpatterns = [
    path('<username>', UpdateUserView.as_view(), name='profile'),
    path('info/<username>', UpdateProfileView.as_view(), name='info'),
]
