# -*- coding:utf-8 -*-

import base
from web import models

# 向数据库添加数据：连接数据库，操作，关闭连接


def run():
    exists = models.PricePolicy.objects.filter(category=1, title='个人免费版').exists()
    if not exists:
        models.PricePolicy.objects.create(
            category=1,
            title='个人免费版',
            price=0,
            project_num=3,
            project_member=2,
            project_space=20,
            per_file_size=5)


if __name__ == '__main__':
    run()