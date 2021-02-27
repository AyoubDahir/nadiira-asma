from django.urls import path

from apps.company.views import CreateWorkerProfile, CompanyList, CompanyDetail, WorkerProfileList, UpdateWorkerProfile, \
    DeleteWorkerProfile, CompanyManagement, WarehouseList, CreateWarehouse, DeleteWarehouse, UpdateWarehouse

app_name = 'company'

urlpatterns = [
    path('manage/addworker/', CreateWorkerProfile.as_view(), name='addworker'),
    path('manage/workers/', WorkerProfileList.as_view(), name='listworkers'),
    path('manage/editworker/<pk>/', UpdateWorkerProfile.as_view(), name='updateworker'),
    path('manage/deleteworker/<pk>/', DeleteWorkerProfile.as_view(), name='deleteworker'),

    path('manage/addwarehouse/', CreateWarehouse.as_view(), name='addwarehouse'),
    path('manage/warehouses/', WarehouseList.as_view(), name='listwarehouse'),
    path('manage/editwarehouse/<pk>/', UpdateWarehouse.as_view(), name='updatewarehouse'),
    path('manage/deletewarehouse/<pk>/', DeleteWarehouse.as_view(), name='deletewarehouse'),

    path('manage/', CompanyManagement.as_view(), name='manage'),

    path('<pk>/', CompanyDetail.as_view(), name='detail'),

    path('', CompanyList.as_view(), name='list'),

]
