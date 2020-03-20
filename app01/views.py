from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

# Create your views here.
import random
from utils.tencent.sms import send_sms_single


def send_sms(request):
    """发送短信"""
    tpl = request.GET.get('tpl')
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    if not template_id:
        return HttpResponse('模板不存在')
    code = random.randrange(1000, 9999)
    res = send_sms_single('18830292815', 559464, [code, ])
    if res['result'] == 0:
        return HttpResponse('发送成功')
    else:
        return HttpResponse('errmsg')
