from django.db import models

# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名', db_index=True)
    password = models.CharField(max_length=32, verbose_name='密码')
    email = models.EmailField(max_length=32, verbose_name='邮箱')
    phone = models.CharField(max_length=11, verbose_name='手机号')
