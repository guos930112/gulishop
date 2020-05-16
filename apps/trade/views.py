from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import time
import random
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_sn = self.get_order_sn()
        order = OrderInfo()
        order.user = self.request.user
        order.order_mount = serializer.validated_data['order_mount']
        order.signer_name = serializer.validated_data['signer_name']
        order.signer_mobile = serializer.validated_data['signer_mobile']
        order.address = serializer.validated_data['address']
        order.order_sn = order_sn
        order.save()

        # 创建完订单 把订单商品表创建完 即把购物车里商品映射
        cart_list = ShopCart.objects.filter(user=self.request.user)
        for cart in cart_list:
            order_goods = OrderGoods()
            order_goods.order = order
            order_goods.goods = cart.goods
            order_goods.goods_num = cart.nums
            order_goods.save()

        # 清空购物车
        cart_list.delete()

        # 生成支付订单链接 加入到返回数据中，可以让前端请求支付链接
        # 创建订单的时候，我们需要调用支付宝的接口，生成一个次订单对应的支付链接，然后返回给前端，前端拿到链接 window.location.href=link 去发送支付请求
        # 支付完成 我们需要对支付后的返回信息进行验签处理，完善订单交易流水号，支付时间等信息

        # 支付宝沙箱环境：公/私钥 appid  数据完善后 支付成功后回到订单页面

        serializer = self.get_serializer_class()(order)  # 手动序列化 因为要返回的数据字段比较少
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_order_sn(self):
        order_sn = '{tm_ms}{userid}{num}'.format(tm_ms=time.strftime("%Y%m%d%H%M%S"), userid=str(self.request.user.id),
                                                 num=str(random.randint(100, 999)))
        return order_sn
