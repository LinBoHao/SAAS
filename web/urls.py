# -*- coding:utf-8 -*-

from django.conf.urls import url, include
from django.views.generic import RedirectView

from web.views import account, project, statistics, wiki, file, setting, issues, dashboard

urlpatterns = [

    url(r'register/$', account.register, name='register'),
    url(r'send/sms/$', account.send_sms, name='send_sms'),
    url(r'login/sms/$', account.login_sms, name='login_sms'),
    url(r'login/$', account.login, name='login'),
    url(r'image/code/', account.image_code, name='image_code'),
    url(r'index/$', account.index, name='index'),
    url(r'logout/$', account.logout, name='logout'),

    # 项目列表
    url(r'^project/list/$', project.project_list, name='project_list'),
    url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)$', project.project_star, name='project_star'),
    url(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)$', project.project_unstar, name='project_unstar'),

    # 项目管理
    url(r'^manage/(?P<project_id>\d+)/', include([

        url(r'^statistics/$', statistics.statistics, name='statistics'),
        url(r'^statistics/priority/$', statistics.statistics_priority, name='statistics_priority'),
        url(r'^statistics/project/user/$', statistics.statistics_project_user, name='statistics_project_user'),

        url(r'^file/$', file.file, name='file'),
        url(r'^file/delete/$', file.file_delete, name='file_delete'),
        url(r'^file/post/$', file.file_post, name='file_post'),
        url(r'^file/download/(?P<file_id>\d+)/$', file.file_download, name='file_download'),
        url(r'^cos/credential/$', file.cos_credential, name='cos_credential'),

        url('^issues/$', issues.issues, name='issues'),
        url('^issues/detail/(?P<issues_id>\d+)/$', issues.issues_detail, name='issues_detail'),
        url('^issues/record/(?P<issues_id>\d+)/$', issues.issues_record, name='issues_record'),
        url('^issues/change/(?P<issues_id>\d+)/$', issues.issues_change, name='issues_change'),
        url('^issues/invite/url/$', issues.invite_url, name='invite_url'),

        url('^dashboard/$', dashboard.dashboard, name='dashboard'),
        url('^dashboard/issues/chart/$', dashboard.issues_chart, name='issues_chart'),

        url(r'^wiki/$', wiki.wiki, name='wiki'),
        url(r'^wiki/add/$', wiki.wiki_add, name='wiki_add'),
        url(r'^wiki/catalog/$', wiki.catalog, name='wiki_catalog'),
        url(r'^wiki/delete/(?P<wiki_id>\d+)/$', wiki.delete, name='wiki_delete'),
        url(r'^wiki/edit/(?P<wiki_id>\d+)/$', wiki.edit, name='wiki_edit'),
        url(r'^wiki/upload/$', wiki.upload, name='wiki_load'),

        url(r'^setting/$', setting.setting, name='setting'),
        url(r'^setting/delete/$', setting.delete, name='setting_delete'),], namespace='manage'), ),

        url('^invite/url/(?P<code>\w+)$', issues.invite_join, name='invite_join'),

]
