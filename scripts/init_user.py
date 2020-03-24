# -*- coding:utf-8 -*-
import base

from web import models

# 向数据库添加数据：连接数据库，操作，关闭连接
models.UserInfo.objects.create(username='陈硕', email='chenshuo@live.com', phone='13838383838', password='12345678')
