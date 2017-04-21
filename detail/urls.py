# !/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from detail import views

urlpatterns=[
    url(r'^detail/$',views.detail,name='detail'),
    url(r'^comment([0-9]*)/$',views.comment,name='comment'),
    url(r'^addcart/$',views.addcart,name='addcart'),
]