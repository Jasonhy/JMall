# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from register2login import views,viewsUtils

urlpatterns = [
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.login,name='login'),
    url(r'^verifycode/$',viewsUtils.verifycode,name='verifycode'),
    url(r'^changekw/$',views.changekw,name='changekw'),
]