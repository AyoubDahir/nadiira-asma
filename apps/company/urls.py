from django.urls import path

from apps.company.views import CreateWorkerProfile, CompanyList, CompanyDetail, WorkerProfileList, UpdateWorkerProfile, \
    DeleteWorkerProfile

app_name = 'company'

urlpatterns = [
    path('manage/addworker/', CreateWorkerProfile.as_view(), name='addworker'),
    path('manage/workers/', WorkerProfileList.as_view(), name='listworkers'),
    path('manage/editworker/<pk>/', UpdateWorkerProfile.as_view(), name='updateworker'),
    path('manage/deleteworker/<pk>/', DeleteWorkerProfile.as_view(), name='deleteworker'),

    path('<pk>', CompanyDetail.as_view(), name='detail'),

    path('', CompanyList.as_view(), name='list'),

]
