from django.urls import path

from apps.company.views import CreateWorkerProfile, WorkerProfileList, UpdateWorkerProfile, \
    DeleteWorkerProfile, WarehouseList, CreateWarehouse, DeleteWarehouse, UpdateWarehouse, \
    CreateTransport, TransportList, UpdateTransport, DeleteTransport, CreateSending, SendingList, UpdateSending, \
    DeleteSending, ApplicationListManage, UpdateApplicationManage, OrderDetailManage, SendingDetail, CreateTransitPoint, \
    DeleteTransitPoint, UpdateTransitPoint

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

    path('manage/addtransport/', CreateTransport.as_view(), name='addtransport'),
    path('manage/transports/', TransportList.as_view(), name='listtransport'),
    path('manage/edittransport/<pk>/', UpdateTransport.as_view(), name='updatetransport'),
    path('manage/deletetransport/<pk>/', DeleteTransport.as_view(), name='deletetransport'),

    path('manage/addsending/', CreateSending.as_view(), name='addsending'),
    path('manage/sendings/', SendingList.as_view(), name='listsending'),
    path('manage/editsending/<pk>/', UpdateSending.as_view(), name='updatesending'),
    path('manage/deletesending/<pk>/', DeleteSending.as_view(), name='deletesending'),
    path('manage/sendingdetail/<pk>/', SendingDetail.as_view(), name='sendingdetail'),

    path('manage/applications/', ApplicationListManage.as_view(), name='listapplicationmanage'),
    path('manage/editapplication/<pk>/', UpdateApplicationManage.as_view(), name='updateapplicationmanage'),

    path('manage/addpoint/<pk>/', CreateTransitPoint.as_view(), name='addpoint'),
    path('manage/deletepoint/<pk>/', DeleteTransitPoint.as_view(), name='deletepoint'),
    path('manage/editpoint/<pk>/', UpdateTransitPoint.as_view(), name='updatepoint'),

    path('manage/orderdetail/<pk>/', OrderDetailManage.as_view(), name='detailordermanage'),

]
