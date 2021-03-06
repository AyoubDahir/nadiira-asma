from django.urls import path

from apps.main.views import MainPageView, OrderList, CreateOrder, UpdateOrder, DeleteOrder, OrderSendings

app_name = 'main'
urlpatterns = [
    path('orders/', OrderList.as_view(), name='orders'),
    path('orders/addorder/', CreateOrder.as_view(), name='addorder'),
    path('orders/editorder/<pk>', UpdateOrder.as_view(), name='updateorder'),
    path('orders/deleteorder/<pk>', DeleteOrder.as_view(), name='deleteorder'),
    path('orders/ordersendings/<pk>', OrderSendings.as_view(), name='ordersendings'),

    path('', MainPageView.as_view(), name='index'),
]
