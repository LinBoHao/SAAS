# -*- coding:utf-8 -*-

from django.conf.urls import url
from web.views import account, home

urlpatterns = [
    url(r'register/$', account.register, name='register'),
    url(r'send/sms/$', account.send_sms, name='send_sms'),
    url(r'login/sms/$', account.login_sms, name='login_sms'),
    url(r'login/$', account.login, name='login'),
    url(r'image/code/', account.image_code, name='image_code'),
    url(r'index/$', home.index, name='index'),
    url(r'logout/$', account.logout, name='logout'),
]

