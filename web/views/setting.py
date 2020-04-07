# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect

from utils.tencent.cos import delete_bucket
from web import models


def setting(request, project_id):
    return render(request, 'setting.html')


def delete(request, project_id):
    if request.method == 'GET':
        return render(request, 'setting_delete.html')

    project_name = request.POST.get('project_name')
    if not project_name or project_name != request.tracer.project.name:
        return render(request, 'setting_delete.html', {'error': '项目名错误'})
    if request.tracer.user != request.tracer.project.creator:
        return render(request, 'setting_delete.html', {'error': '只有项目创建者才能删除项目'})

    # 删除桶
    delete_bucket(request.tracer.project.bucket, request.tracer.project.region)
    # 删除项目
    models.Project.objects.filter(id=project_id).delete()

    return redirect('web:project_list')
