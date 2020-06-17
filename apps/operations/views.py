from django.shortcuts import render
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavListSerializer, UserLeavingMessageSerializer, UserAddressSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly


# Create your views here.


class UserFavViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    # 登陆权限/ 操作 收藏的权限
    lookup_field = 'goods_id'  # 我们要把商品id给到前端 但是 不配置的话返回的是 userfav对象的id 和前端不匹配，前端是商品id

    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # 重写 get_queryset 方法  因为前端 拿的是商品id  而表里 这个商品可以被多个用户收藏所以需要指定登陆的用户
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """
            动态配置序列化
        :return:
        """
        if self.action == 'list':
            return UserFavListSerializer
        return UserFavSerializer

    def create(self, request, *args, **kwargs):
        """
            增加收藏
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)  # 可以返回一个实例
        instance.goods.fav_num += 1
        instance.goods.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
            重写 perform_create 方法
        :param serializer:
        :return:
        """
        return serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
            取消收藏
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        instance.goods.fav_num -= 1
        instance.goods.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLeavingMessageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = UserLeavingMessageSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class UserAddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
