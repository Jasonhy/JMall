# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from index import views

urlpatterns = [
    url(r'^index/$',views.index,name='indexPage'),
    url(r'^loginOut/$',views.loginOut,name='loginOut'),
]