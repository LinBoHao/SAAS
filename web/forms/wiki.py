# -*- coding:utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from web import models
from web.forms.BootStrapForm import BootStrapForm


class WikiModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Wiki
        exclude = ['project', ]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

        # 找到字段， 绑定数据重置
        total_data_list = [('', '请选择'), ]
        data_list = models.Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title')
        total_data_list.extend(data_list)
        self.fields['parent'].choices = total_data_list

