from django.core.validators import RegexValidator
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

# Create your views here.
import random
from utils.tencent.sms import send_sms_single
from django import forms
from app01 import models


class RegisterModelForm(forms.ModelForm):
    phone = forms.CharField(label='手机号', validators=[RegexValidator
                                                     (r'^(1[3\4\5\6\7\8\9])\d{9}$', '手机号格式错误'), ])
    password = forms.CharField(label='密  码', widget=forms.PasswordInput
    (attrs={'class': 'form-control', 'placeholder': '输入密码'}))
    confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput
    (attrs={'class': 'form-control', 'placeholder': '重复密码'}))
    code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入验证码'}))

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'phone', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)


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


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})
