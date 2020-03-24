# -*- coding:utf-8 -*-
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from web import models


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """如果用户已登录，则在request中赋值"""
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.SAAS = user_object

        # 白名单：没有登陆也可以访问的URL
        """
        1.获取当前用户访问的URL
        2.检查URL是否再把名单中，如果在，则可以继续访问，如果不在，进行判断是否在白名单中
        """
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        if not request.SAAS:
            return redirect('web:login')