from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_home, name='order_home'),
    path('create_order', views.create_order, name='create_order'),
    path('pay_order', views.pay_order, name='pay_order'),
    path('fulfill_order', views.fulfill_order, name='fulfill_order'),
    path('cancel_order', views.cancel_order, name='cancel_order'),
    path('return_order', views.return_order, name='return_order'),
]
