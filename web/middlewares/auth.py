# -*- coding:utf-8 -*-

import datetime

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from web import models


class Tracer(object):
    def __int__(self):
        self.user = None
        self.price_policy = None


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.tracer = Tracer()
        """如果用户已登录，则在request中赋值"""
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer.user = user_object

        # 白名单：没有登陆也可以访问的URL
        """
        1.获取当前用户访问的URL
        2.检查URL是否再把名单中，如果在，则可以继续访问，如果不在，进行判断是否在白名单中
        """
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        if not request.tracer.user:
            return redirect('web:login')
        """
        登陆成功后，访问后台管理时，获取当前用户所拥有的额度
        获取当前用户ID值最大
        """
        _object = models.Transaction.objects.filter(user=user_object).order_by('-id').first()
        current_time = datetime.datetime.now()
        if _object.end_datetime and _object.end_datetime < current_time:
            # 过期
            _object = models.Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).first()

        request.tracer.price_policy = _object.price_policy
