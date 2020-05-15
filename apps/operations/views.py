from django.shortcuts import render
from rest_framework import mixins, viewsets
from .models import UserFav
from .serializers import UserFavSerializer
# Create your views here.


class UserFavViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    # 登陆权限/ 操作 收藏的权限
    lookup_field = 'goods_id'  # 我们要把商品id给到前端 但是 不配置的话返回的是 userfav对象的id 和前端不匹配，前端是商品id
