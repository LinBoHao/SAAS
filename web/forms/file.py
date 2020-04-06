# -*- coding:utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from utils.tencent.cos import check_file
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


class FileModelForm(forms.ModelForm):
    etag = forms.CharField(label='ETag')

    class Meta:
        model = models.FileRepository
        exclude = ['project', 'file_type', 'update_user', 'update_time']

    def __init__(self, request, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.request = request

    def clean_file_path(self):
        return f'https://{self.cleaned_data["file_path"] }'

    # def clean(self):
    #     etag = self.cleaned_data['etag']
    #     key = self.cleaned_data['key']
    #     size = self.cleaned_data['size']
    #     if not key or not etag:
    #         return self.cleaned_data
    #     # 向COS检验文件是否合法
    #     from qcloud_cos.cos_exception import CosServiceError
    #     try:
    #         result = check_file(self.request.tracer.project.bucket, self.request.tracer.project.region, key)
    #     except CosServiceError as e:
    #         self.add_error(key, '文件不存在')
    #         return self.cleaned_data
    #     cos_etag = result.get('ETag')
    #     if cos_etag != etag:
    #         self.add_error('etag', 'ETag错误')
    #     con_length = result.get('Content-Length')
    #     if int(con_length) != size:
    #         self.add_error('size', '文件大小错误')
    #
    #     return self.cleaned_data



