# -*- coding:utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from web import models
from web.forms.BootStrapForm import BootStrapForm
from web.forms.widgets import ColorSelect


class ProjectModelForm(BootStrapForm, forms.ModelForm):

    bootstrap_class_exclude = ['color']

    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {
            'desc': forms.Textarea,
            'color': ColorSelect(attrs={'class': 'color-radio'}),
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        """项目校验"""
        # 1.当前用户是否已创建过此项目
        name = self.cleaned_data['name']
        user = self.request.tracer.user
        exists = models.Project.objects.filter(name=name, creator=user).exists()
        if exists:
            raise ValidationError('项目名已存在')
        # 2.当前用户是否还有额度进行创建项目
        project_num = self.request.tracer.price_policy.project_num
        count = models.Project.objects.filter(creator=user).count()

        if count >= project_num:
            raise ValidationError('项目个数超限，请购买套餐')

        return name

