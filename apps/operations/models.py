from django.db import models
from users.models import UserProfile
from goods.models import Goods
from datetime import datetime


# Create your models here.

class UserFav(models.Model):
    """
        用户收藏表
    """
    user = models.ForeignKey(UserProfile, verbose_name='所属用户')
    goods = models.ForeignKey(Goods, verbose_name='所属商品')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = '用户收藏信息'
        verbose_name_plural = verbose_name


class UserLeavingMessage(models.Model):
    """
        用户留言表
    """
    MSG_TYPE = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购"),

    )
    user = models.ForeignKey(UserProfile, verbose_name='所属用户')
    msg_type = models.IntegerField(choices=MSG_TYPE, default=1, verbose_name='留言类型')
    subject = models.CharField(max_length=30, verbose_name='留言主题')
    message = models.CharField(max_length=300, verbose_name='留言内容')
    file = models.FileField(upload_to='users/files', max_length=200, verbose_name='留言文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = '用户留言信息'
        verbose_name_plural = verbose_name


class UserAddress(models.Model):
    """
        用户收货地址信息表
    """
    user = models.ForeignKey(UserProfile, verbose_name='所属用户')
    province = models.CharField(max_length=50, verbose_name='省')
    city = models.CharField(max_length=50, verbose_name='市')
    district = models.CharField(max_length=50, verbose_name='区')
    signing_name = models.CharField(max_length=20, verbose_name="收货人")
    signing_mobile = models.CharField(max_length=11, verbose_name="收货电话")
    address = models.CharField(max_length=300, verbose_name="收货地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.signing_name

    class Meta:
        verbose_name = '用户收货地址信息'
        verbose_name_plural = verbose_name
