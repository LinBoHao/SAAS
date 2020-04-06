# -*- coding:utf-8 -*-
import json

from django.http import JsonResponse
from django.shortcuts import render

from web import models
from utils.tencent.cos import delete_file, delete_file_list, credential
from web.forms.file import FileFolderModelForm, FileModelForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def file(request, project_id):

    parent_object = None
    folder_id = request.GET.get('folder', '')
    if folder_id.isdecimal():
        parent_object = models.FileRepository.objects.filter(id=int(folder_id),
                                                             file_type=2, project=request.tracer.project).first()

    """文件列表&新建文件夹"""
    if request.method == "GET":

        # 当前目录下所有的文件&文件夹获取

        breadcrumb_list = []
        parent = parent_object
        while parent:
            breadcrumb_list.insert(0, {'id': parent.id, 'name': parent.name})
            parent = parent.parent

        query_set = models.FileRepository.objects.filter(project=request.tracer.project)
        if not parent_object:
            file_object_list = query_set.filter(parent__isnull=True).order_by('-file_type')
        else:
            file_object_list = query_set.filter(parent=parent_object).order_by('-file_type')
        form = FileFolderModelForm(request, parent_object)
        context = {
            'form': form,
            'file_object_list': file_object_list,
            'breadcrumb_list': breadcrumb_list,
            'folder_object': parent_object,
        }
        return render(request, 'file.html', context)

    # 添加文件夹&文件夹的修改

    fid = request.POST.get('fid', '')
    edit_object = None
    if fid.isdecimal():
       edit_object = models.FileRepository.objects.filter(id=int(fid), file_type=2, project=request.tracer.project).first()
    if edit_object:
        form = FileFolderModelForm(request, parent_object, data=request.POST, instance=edit_object)
    else:
        form = FileFolderModelForm(request, parent_object, data=request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.update_user = request.tracer.user
        form.instance.file_type = 2
        form.instance.parent = parent_object
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def file_delete(request, project_id):
    """删除文件
       级联删除"""
    fid = request.GET.get('fid')
    delete_object = models.FileRepository.objects.filter(id=fid, project=request.tracer.project).first()
    if delete_object.file_type == 1:
        # 删除文件
        request.tracer.project.use_space -= delete_object.file_size
        request.tracer.project.save()

        # cos中删除文件
        delete_file(request.tracer.project.bucket, request.tracer.project.region, delete_object.key)
        delete_object.delete()
        return JsonResponse({'status': True})

    else:
        # 删除文件夹
        models.FileRepository.objects.filter(parent=delete_object)
        total_size = 0
        folder_list = [delete_object]
        key_list = []
        for folder in folder_list:
            child_list = models.FileRepository.objects.filter(project=request.tracer.project, parent=folder).order_by('-file_type')
            for child in child_list:
                if child.file_type == 2:
                    folder_list.append(child)
                else:
                    total_size += child.file_size
                    # 删除文件
                    key_list.append({'Key': child.key})

        if key_list:
            delete_file_list(request.tracer.project.bucket, request.tracer.project.region, key_list)
        if total_size:
            request.tracer.project.use_space -= total_size
            request.tracer.project.save()
        delete_object.delete()

@csrf_exempt
def cos_credential(request, project_id):
    # 获取cos上传临时凭证& 做容量限制：单文件&总容量
    file_list = json.loads(request.body.decode('utf-8'))
    per_file_limit = request.tracer.price_policy.per_file_size * 1024 * 1024
    total_file_limit = request.tracer.price_policy.per_file_size * 1024 * 1024 * 1024

    total_size = 0
    for item in file_list:
        if item['size'] > per_file_limit:
            name = item['name']
            return JsonResponse({
                'status': False,
                'error': f'单文件超出限制(最大{request.tracer.price_policy.per_file_size}M, 文件:{name})'})
        total_size += item['size']
    if total_size + request.tracer.project.use_space > total_file_limit:
        return JsonResponse({
            'status': False,
            'error': '容量超出限制, 请升级套餐'})

    data_dict = credential(request.tracer.project.bucket, request.tracer.project.region,)
    return JsonResponse({'status': True, 'data': data_dict})

@csrf_exempt
def file_post(request, project_id):
    # 将上传成功的文件写入到数据库
    print(request.POST)
    # 把获取到的数据写入到数据库
    form = FileModelForm(request, data=request.POST)
    if form.is_valid():
        data_dict = form.cleaned_data
        data_dict.pop('etag')
        data_dict.update({'project': request.tracer.project, 'file_type': 1, 'update_user': request.tracer.user})
        instance = models.FileRepository.objects.create(**data_dict)

        # 项目的一使用空间：更新
        request.tracer.project.use_space += data_dict['file_size']
        result = {
            'id': instance.id,
            'name': instance.name,
            'file_size': instance.file_size,
            'username': instance.update_user.username,
            'datetime': instance.update_time.strftime('%Y年-%m月-%d日 %H:%M')
        }
        return JsonResponse({'status': True, 'data': result})

    return JsonResponse({'status': False, 'data': '文件错误'})