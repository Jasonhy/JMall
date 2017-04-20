# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from usercenter import views

urlpatterns = [
    url(r'^user_center_info/$',views.user_center_info,name='user_center_info'),
]