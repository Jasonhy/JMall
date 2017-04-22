# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from goodslist import views
urlpatterns = [
    url(r'^list/$',views.list,name='list'),
]