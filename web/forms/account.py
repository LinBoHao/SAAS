# -*- coding:utf-8 -*-
import random

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms

from django.conf import settings
from utils.tencent.sms import send_sms_single
from web import models
from django_redis import get_redis_connection
from utils.encrypt import md5


class SendSmsForm(forms.Form):
    phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # 校验数据库中是否已有手机号
        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError('短信模板错误')
        exists = models.UserInfo.objects.filter(phone=phone).exists()
        if exists:
            raise ValidationError('手机号已存在')

        code = random.randrange(1000, 9999)
        sms = send_sms_single(phone, template_id, [code, 1])
        if sms['result'] != 0:
            raise ValidationError('短信发送失败, {}'.format(sms['errmsg']))
        conn = get_redis_connection('default')
        conn.set(phone, code, ex=60)

        return phone


class RegisterModelForm(forms.ModelForm):
    phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    password = forms.CharField(label='密  码', widget=forms.PasswordInput
    (attrs={'class': 'form-control', 'placeholder': '输入密码'}), min_length=8, max_length=64, error_messages={
        'min_length': '密码长度不能小于8个字符',
        'max_length': '密码长度不能大于64个字符',
    })
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

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_password(self):
        pwd = self.cleaned_data['password']

        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data['password']
        confirm_pwd = md5(self.cleaned_data['confirm_password'])
        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')
        return confirm_pwd

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        exists = models.UserInfo.objects.filter(phone=phone).exists()
        if exists:
            raise ValidationError('该手机号已注册')
        return phone

    def clean_code(self):
        code = self.cleaned_data['code']
        phone = self.cleaned_data['phone']

        conn = get_redis_connection('default')
        register_code = conn.get(phone)
        if not register_code:
            raise ValidationError('验证码已失效或未发送，请重新发送')
        register_str_code = register_code.decode('utf-8')
        if code.strip() != register_str_code:
            raise ValidationError('验证码错误，请重新输入')

        return code
