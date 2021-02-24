from django.urls import path

from apps.company.views import CreateWorkerProfile

urlpatterns = [
    path('addworker/', CreateWorkerProfile.as_view()),

]
