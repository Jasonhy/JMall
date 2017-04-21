# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from cart import views

urlpatterns = [
    url(r'^cart/$',views.cart,name='cart'),
    url(r'^deleteHander/$',views.deleteHander,name='deleteHander'),
    url(r'^place_order/$',views.place_order,name='place_order'),
]