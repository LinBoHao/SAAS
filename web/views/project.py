# -*- coding:utf-8 -*-
import time

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from web import models
from web.forms.project import ProjectModelForm
from utils.tencent.cos import create_bucket


def project_list(request):
    if request.method == 'GET':

        user = request.tracer.user
        project_dict = {'star': [], 'my': [], 'join': []}
        my_project = models.Project.objects.filter(creator=user)
        join_project = models.ProjectUser.objects.filter(user=user)

        for row in my_project:
            if row.star:
                project_dict['star'].append({'value': row, 'type': 'my'})
            else:
                project_dict['my'].append(row)
        for item in join_project:
            if item.star:
                project_dict['star'].append({'value': item.project, 'type': 'join'})
            else:
                project_dict['join'].append(item.project)

        form = ProjectModelForm(request)
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})

    form = ProjectModelForm(request, request.POST)
    if form.is_valid():
        # 为项目创建桶
        bucket = "{}-{}-1252704499".format(request.tracer.user.phone, str(int(time.time())))
        region = 'ap-chengdu'
        create_bucket(bucket, region)

        form.instance.bucket = bucket
        form.instance.region = region
        form.instance.creator = request.tracer.user
        instance = form.save()
        issues_type_object_list = []
        for item in models.IssuesType.PROJECT_INIT_LIST:
            issues_type_object_list.append(models.IssuesType(project=instance, title=item))
        models.IssuesType.objects.bulk_create(issues_type_object_list)
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):

    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
        return redirect('web:project_list')
    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)
        return redirect('web:project_list')

    return HttpResponse('请求错误')


def project_unstar(request, project_type, project_id):
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        return redirect('web:project_list')
    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
        return redirect('web:project_list')

    return HttpResponse('请求错误')