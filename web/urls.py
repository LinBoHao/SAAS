# -*- coding:utf-8 -*-

from django.conf.urls import url
from web.views import account

urlpatterns = [
    url(r'register/$', account.register, name='register'),
    url(r'send/sms/$', account.send_sms, name='send_sms')
]

