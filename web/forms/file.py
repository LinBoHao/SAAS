# -*- coding:utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from web import models
from web.forms.BootStrapForm import BootStrapForm


class FileFolderModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.FileRepository
        fields = ['name']

    def __init__(self, request, parent_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.parent_object = parent_object

    def clean_name(self):
        name = self.cleaned_data['name']

        # 数据库判断 当前目录下此文件夹是否已存在
        query_set = models.FileRepository.objects.filter(file_type=2, name=name, project=self.request.tracer.project,)
        if self.parent_object:
            exists = query_set.filter(parent=self.parent_object)
        else:
            exists = query_set.filter(parent__isnull=True)
        if exists:
            raise ValidationError('文件夹已存在')
        return name