from django.shortcuts import render
from random import choice
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from .models import VerifyCode, UserProfile
from .serializers import VerifyCodeSerializer, UserSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from gulishop.settings import YUNPIAN_KEY
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly


# Create your views here.

class VerifyCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = VerifyCode.objects.all()
    serializer_class = VerifyCodeSerializer

    def create(self, request, *args, **kwargs):  # 重写 create, 因为要加发送验证码功能
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 判断是否合法

        mobile = serializer.validated_data['mobile']
        code = self.get_random_code()

        yunpian = YunPian(YUNPIAN_KEY)
        result = yunpian.send_msg(mobile, code)

        if result['code'] == 0:  # 只有发送成功再创建对象
            ver_code = VerifyCode()
            ver_code.code = code
            ver_code.mobile = mobile
            ver_code.save()
            return Response(data={'mobile': mobile, 'msg': result['msg']}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'mobile': mobile, 'msg': result['msg']}, status=status.HTTP_400_BAD_REQUEST)

    def get_random_code(self):
        code_source = '1234567890'
        code = ''
        for i in range(6):
            code += choice(code_source)
        return code


# 用户中心操作必须登陆
class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    # 当用户登陆即显示当前用户不能用全局的认证
    # 认证一般不会配置在settings中进行全局配置，因为当用户token过期不过期都允许用户查看某些资源（商品列表/详情）
    # 我们要在必须验证的资源上局部添加认证信息 SessionAuthentication 是必须配置的 因为要用browser api
    # JSONWebTokenAuthentication 判断token是否过期
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    # 权限 获取信息时才会有权限问题，而创建用户是没有的 所以需要动态配置;  属于具体用户的比如用户中心的一些数据；
    # 那无关用户的一些资源的权限 呢？ IsOwnerOrReadOnly 自定义
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # # 重写获取 认证的方法，创建用户时不需要
    # def get_authenticators(self):
    #     """
    #     Instantiates and returns the list of authenticators that this view can use.
    #     """
    #     if self.action == 'create':
    #         return list()
    #     return [auth() for auth in self.authentication_classes]

    # 3/重写获取 权限的方法
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            return list()
        return [permission() for permission in self.permission_classes]

    # 1/重写get_serializer_class方法， 目的动态配置序列化器 因为创建/获取 返回的信息不同
    def get_serializer_class(self):
        """
            动态配置序列化，用户创建用创建序列化UserSerializer，其余用UserDetailSerializer
        :return:
        """
        if self.action == 'create':
            return UserSerializer
        return UserDetailSerializer

    # 2/重写get_object方法 目的只返回当前登陆的用户 而不是前端随便传的用户id
    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):  # 没有mobile 并且 没有把密码加密
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 如果合法会把 所有传进来的键值对形成字典
        # 进来 验证过后 创建 对象，因为自身的create方法没有把相应的字段补全，密码没有加密
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = UserProfile()
        user.username = username
        user.mobile = username
        user.set_password(password)
        user.save()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        ret = serializer.data
        ret['name'] = user.name if user.name else user.username
        ret['token'] = token
        headers = self.get_success_headers(serializer.data)
        return Response(ret, status=status.HTTP_201_CREATED, headers=headers)  # 这里是出去序列化
