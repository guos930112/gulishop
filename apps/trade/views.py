from django.shortcuts import render, redirect, reverse
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime
import time
import random
from django.db import transaction

from gulishop.settings import private_key, ali_key, app_id
from utils.alipay import AliPay
from utils.permissions import IsOwnerOrReadOnly
from .models import ShopCart, OrderInfo, OrderGoods
from .serializers import ShopCartSerializer, ShopCartListSerializer, OrderInfoSerializer, OrderDetailSerializer


# Create your views here.

class ShopCartViewSet(viewsets.ModelViewSet):  # 增删改查 都有的话 可以直接继承 ModelViewSet

    serializer_class = ShopCartSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShopCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartListSerializer
        return ShopCartSerializer

    # 因为 创建和更改混合在一块 所以需要重写 create方法
    def create(self, request, *args, **kwargs):  # 对同一件商品 只是增加商品 而不是再创建一条数据
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        goods = serializer.validated_data['goods']
        nums = serializer.validated_data['nums']
        cart_list = ShopCart.objects.filter(user=self.request.user, goods=goods)
        if cart_list:
            cart = cart_list[0]
            cart.nums += nums
            cart.save()
        else:
            cart = ShopCart()
            cart.user = self.request.user
            cart.goods = goods
            cart.nums = nums
            cart.save()
        serializer = self.get_serializer_class()(cart)  # 手动序列化
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderInfoViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    # 1 创建订单 2创建订单商品 3清空购物车 4支付

    serializer_class = OrderInfoSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def get_queryset(self):  # 只返回当前登陆用户的数据
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        """
            重写 获取某个订单的方法 因为 用户在支付的过程中 可能直接关闭支付 那这个时候这个订单即为未支付状态，也需要把支付链接返回
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()  # 获取到某个订单实例
        alipay = AliPay(
            appid=app_id,
            app_notify_url="http://47.105.33.27:8000/alipay_return/",
            app_private_key_path=private_key,
            alipay_public_key_path=ali_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.105.33.27:8000/alipay_return/"
        )
        url = alipay.direct_pay(
            subject=instance.order_sn,
            out_trade_no=instance.order_sn,
            total_amount=instance.order_mount
        )
        # 沙箱环境
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        serializer = self.get_serializer(instance)
        ret = serializer.data
        ret['alipay_url'] = re_url
        return Response(ret)

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 创建事物的回退点：
        back_pointer = transaction.savepoint()
        order_sn = self.get_order_sn()
        order = OrderInfo()
        order.user = self.request.user
        order.order_mount = serializer.validated_data['order_mount']
        order.signer_name = serializer.validated_data['signer_name']
        order.signer_mobile = serializer.validated_data['signer_mobile']
        order.address = serializer.validated_data['address']
        order.order_sn = order_sn
        order.save()

        # 创建完订单 把订单商品表创建完 即把购物车里商品映射到订单商品表里
        cart_list = ShopCart.objects.filter(user=self.request.user)
        for cart in cart_list:
            order_goods = OrderGoods()
            order_goods.order = order
            order_goods.goods = cart.goods
            order_goods.goods_num = cart.nums
            if order_goods.goods.goods_num < cart.nums:
                transaction.savepoint_rollback(back_pointer)
                return Response({'msg': '库存不足'}, status=status.HTTP_400_BAD_REQUEST)
            # 减库存
            order_goods.goods.goods_num -= cart.nums
            order_goods.goods.save()
            order_goods.save()

        # 清空购物车
        cart_list.delete()

        transaction.savepoint_commit(back_pointer)

        # 生成支付订单链接 加入到返回数据中，可以让前端请求支付链接
        # 创建订单的时候，我们需要调用支付宝的接口，生成一个次订单对应的支付链接，然后返回给前端，前端拿到链接 window.location.href=link 去发送支付请求
        # 支付完成 我们需要对支付后的返回信息进行验签处理，完善订单交易流水号，支付时间等信息

        # 支付宝沙箱环境：公/私钥 appid  数据完善后 支付成功后回到订单页面
        alipay = AliPay(
            appid=app_id,
            app_notify_url="http://47.105.33.27:8000/alipay_return/",
            app_private_key_path=private_key,
            alipay_public_key_path=ali_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.105.33.27:8000/alipay_return/"  # 这个最终需要配置成线上的
        )
        url = alipay.direct_pay(
            subject=order.order_sn,
            out_trade_no=order.order_sn,
            total_amount=order.order_mount
        )
        # 生成支付链接
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        # serializer = self.get_serializer_class()(order)  # 手动序列化 因为要返回的数据字段比较少
        serializer = self.get_serializer(order)
        headers = self.get_success_headers(serializer.data)
        ret = serializer.data
        ret['alipay_url'] = re_url
        return Response(ret, status=status.HTTP_201_CREATED, headers=headers)

    def get_order_sn(self):
        order_sn = '{tm_ms}{userid}{num}'.format(tm_ms=time.strftime("%Y%m%d%H%M%S"), userid=str(self.request.user.id),
                                                 num=str(random.randint(100, 999)))
        return order_sn


class AliPayView(APIView):
    """
        用来处理： 支付宝：return_url 的请求
    """

    def get(self, request):
        """
            返回哪个页面 即redirect 到订单列表页
        :param request:
        :return:
        """
        data_dict = dict()
        for k, v in request.GET.items():  # 把类字典转换为字典，包括签名
            data_dict[k] = v
        sign = data_dict.pop('sign', None)  # 此时数据只有数据了
        alipay = AliPay(
            appid=app_id,
            app_notify_url="http://47.105.33.27:8000/alipay_return/",
            app_private_key_path=private_key,
            alipay_public_key_path=ali_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.105.33.27:8000/alipay_return/"  # 这个最终需要配置成线上的
        )
        res = alipay.verify(data_dict, sign)
        if res:  # 比对成功即验签成功 返回 True
            # 此时我们可以更新订单流水号等信息
            order_sn = data_dict.get('out_trade_no', '')
            trade_no = data_dict.get('trade_no', '')
            pay_time = datetime.now()
            pay_status = data_dict.get('trade_status', 'TRADE_SUCCESS')
            order_list = OrderInfo.objects.filter(order_sn=order_sn)
            if order_list:
                order = order_list[0]
                order.pay_status = pay_status
                order.pay_time = pay_time
                order.trade_no = trade_no
                order.save()
                ret = redirect(reverse('index'))
                ret.set_cookie('nextPath', 'pay', 2)
                return ret

    def post(self, request):
        """
            做验证 返回 success 状态 确认是否付款成功
            支付成功后 回传的信息要验签通过 才可以完善订单， 防止恶意攻击
        :param request:
        :return:
        """
        data_dict = dict()
        for k, v in request.POST.items():  # 把类字典转换为字典，包括签名
            data_dict[k] = v
        sign = data_dict.pop('sign', None)  # 此时数据只有数据了
        alipay = AliPay(
            appid=app_id,
            app_notify_url="http://47.105.33.27:8000/alipay_return/",
            app_private_key_path=private_key,
            alipay_public_key_path=ali_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.105.33.27:8000/alipay_return/"  # 这个最终需要配置成线上的
        )
        res = alipay.verify(data_dict, sign)
        if res:  # 比对成功即验签成功 返回 True
            # 此时我们可以更新订单流水号等信息
            order_sn = data_dict.get('out_trade_no', '')
            trade_no = data_dict.get('trade_no', '')
            pay_time = datetime.now()
            pay_status = data_dict.get('trade_status', 'TRADE_SUCCESS')
            order_list = OrderInfo.objects.filter(order_sn=order_sn)
            if order_list:
                order = order_list[0]
                order.pay_status = pay_status
                order.pay_time = pay_time
                order.trade_no = trade_no
                order.save()
                # 支付成功要把销量加上 主表.字表类名小写.all() 返回的是一个列表
                order_goods_list = order.goods.all()
                for order_goods in order_goods_list:
                    order_goods.goods.sold_num += order_goods.goods_num
                    order_goods.save()
                return Response('success')
