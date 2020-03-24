# -*- coding:utf-8 -*-
import uuid
import datetime

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from web import models
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSmsForm, LoginForm


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过，写入数据库
        instance = form.save()
        # 创建交易记录
        policy_project = models.PricePolicy.objects.filter(category=1, title='个人免费版')
        models.Transaction.objects.create(status=2,
                                          order=str(uuid.uuid4()),
                                          user=instance,
                                          price_policy=policy_project,
                                          count=0,
                                          price=0,
                                          start_datetime=datetime.datetime.now())
        return JsonResponse({'status': True, 'data': '/login/'})

    return JsonResponse({'status': False, 'error': form.errors})


def send_sms(request):
    # 发送短信
    form = SendSmsForm(request, data=request.GET)
    # 只是校验手机号， 不能为空，格式是否正确

    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    if request.method == 'GET':
        form = LoginSmsForm()
        return render(request, 'login_sms.html', {'form': form})
    form = LoginSmsForm(data=request.POST)
    if form.is_valid():
        phone = form.cleaned_data['phone']
        user_object = models.UserInfo.objects.filter(phone=phone).first()
        request.session['user_id'] = user_object.id
        request.session.set_expiry(60 * 60 * 24 * 14)
        return JsonResponse({'status': True, 'data': '/index/'})

    return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    """"用户名密码登录"""
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user_object = models.UserInfo.objects.filter(Q(email=username)|Q(phone=username)).\
            filter(password=password).first()
        if user_object:
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60*60*24*14)
            return redirect('web:index')
        form.add_error('username', '用户名或密码错误')
    return render(request, 'login.html', {'form': form})


def image_code(request):
    """生成图片验证码"""
    from utils.image_code import check_code
    from io import BytesIO

    image_object, code = check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)
    # 修改session过期时间
    stream = BytesIO()
    image_object.save(stream, 'png')
    stream.getvalue()
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('web:index')