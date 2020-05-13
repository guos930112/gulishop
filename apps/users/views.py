from django.shortcuts import render
from random import choice
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from .models import VerifyCode, UserProfile
from .serializers import VerifyCodeSerializer, UserSerializer
from utils.yunpian import YunPian
from gulishop.settings import YUNPIAN_KEY


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


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

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
