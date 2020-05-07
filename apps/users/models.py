from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.


class UserProfile(AbstractUser):
    """
        用户信息表
    """
    name = models.CharField(max_length=50, verbose_name='用户姓名', null=True, blank=True)  # 注册时可以不填名字
    birthday = models.DateField(verbose_name='用户生日', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女')), default='female',
                              verbose_name='用户性别', help_text='表示用户的性别')
    mobile = models.CharField(max_length=11, verbose_name='用户手机', null=True, blank=True, help_text='表示用户手机')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='表示用户的添加时间')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class VerifyCode(models.Model):
    """
        手机验证码表
    """
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='验证手机')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '手机验证码信息'
        verbose_name_plural = verbose_name
