from django.db import models
from users.models import UserProfile
from goods.models import Goods
from datetime import datetime


# Create your models here.


class ShopCart(models.Model):
    '''
        购物车： 谁买谁 买了几件
    '''
    user = models.ForeignKey(UserProfile, verbose_name='所属用户')
    goods = models.ForeignKey(Goods, verbose_name='所属商品')
    nums = models.IntegerField(verbose_name='购买数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = '购物车信息'
        verbose_name_plural = verbose_name


class OrderInfo(models.Model):
    """
        订单表
    """
    ORDER_STATUS = (
        ("PAYING", "待支付"),
        ("TRADE_SUCESS", "支付成功"),
        ("TRADE_CLOSE", "支付关闭"),
        ("TRADE_FAIL", "支付失败"),
        ("TRADE_FINSHED", "交易结束"),
    )
    # 第一部分，订单最基本的部分
    user = models.ForeignKey(UserProfile, verbose_name='所属用户')
    order_sn = models.CharField(max_length=50, verbose_name='订单唯一编号', unique=True)
    order_amount = models.FloatField(verbose_name='订单总价')
    order_message = models.CharField(max_length=300, verbose_name='订单留言', null=True, blank=True)

    # 第二部分,订单支付部分
    trade_no = models.CharField(max_length=50, verbose_name='交易流水号', unique=True, null=True, blank=True,
                                help_text='支付宝支付成功会返回流水号')  # 支付成功后支付宝返回的
    trade_status = models.CharField(max_length=20, verbose_name='订单状态', choices=ORDER_STATUS, default='PAYING')
    pay_time = models.DateTimeField(verbose_name='支付时间', null=True, blank=True)

    # 第三部分，订单收货人信息
    signing_name = models.CharField(max_length=30, verbose_name="签收人")
    # 签收电话
    signing_mobile = models.CharField(max_length=11, verbose_name="联系电话")
    # 签收地址
    address = models.CharField(max_length=200, verbose_name="收货地址")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.order_sn

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name


class OrderGoods(models.Model):
    """
        订单商品表
    """
    order = models.ForeignKey(OrderInfo, verbose_name="所属订单")
    goods = models.ForeignKey(Goods, verbose_name="所属商品")
    nums = models.IntegerField(verbose_name="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = '订单商品信息'
        verbose_name_plural = verbose_name
