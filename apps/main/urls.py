from django.urls import path

from apps.main.views import MainpageView

app_name = 'main'
urlpatterns = [
    path('', MainpageView.as_view(), name='index'),
]
