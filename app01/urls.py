# -*- coding:utf-8 -*-


from django.conf.urls import url, include

from app01 import views

urlpatterns = [
    url(r'^register/', views.register, name='app01_register')
]
