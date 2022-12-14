from django.urls import path

from apps.main.views import MainPageView, OrderList, CreateOrder, UpdateOrder, DeleteOrder, OrderSendings, \
    CreateApplication, ApplicationList, DeleteApplication, CompanyDetail, CompanyList

app_name = 'main'
urlpatterns = [
    path('orders/', OrderList.as_view(), name='orders'),
    path('orders/addorder/', CreateOrder.as_view(), name='addorder'),
    path('orders/editorder/<pk>', UpdateOrder.as_view(), name='updateorder'),
    path('orders/deleteorder/<pk>', DeleteOrder.as_view(), name='deleteorder'),
    path('orders/ordersendings/<pk>', OrderSendings.as_view(), name='ordersendings'),

    path('application/deleteapplication/<pk>', DeleteApplication.as_view(), name='deleteapplication'),
    path('application/<order_pk>/<sending_pk>', CreateApplication.as_view(), name='addaplication'),
    path('applications/', ApplicationList.as_view(), name='applications'),

    path('companies/<pk>/', CompanyDetail.as_view(), name='company_detail'),
    path('companies/', CompanyList.as_view(), name='company_list'),

    path('', MainPageView.as_view(), name='index'),
]
