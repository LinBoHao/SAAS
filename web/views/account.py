# -*- coding:utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from web.forms.account import RegisterModelForm, SendSmsForm


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过，写入数据库
        form.save()
        return JsonResponse({'status': True, 'data': '/login/'})

    return JsonResponse({'status': False, 'data': form.errors})



def send_sms(request):

    # 发送短信
    form = SendSmsForm(request, data=request.GET)
    # 只是校验手机号， 不能为空，格式是否正确

    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})