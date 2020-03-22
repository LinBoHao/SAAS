# -*- coding:utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from web.forms.account import RegisterModelForm, SendSmsForm


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})


def send_sms(request):
    # 发送短信
    form = SendSmsForm(request, data=request.GET)
    # 只是校验手机号， 不能为空，格式是否正确

    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})