from django.shortcuts import render, HttpResponse
from django.views import View
from .models import Goods, GoodsCategory, Banner
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from django.core.paginator import Paginator
from rest_framework.views import APIView
from .serializers import GoodsSerializer, CategorySerializer, IndexBannerSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins, pagination, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter
import logging
from config.env_config import CUR_ENV


# class GoodsView(View):
#     def get(self, request):
#         all_goods = Goods.objects.all()  # query list
#         # query类型转为dict
#         # 第一种序列化 python内置 json库来实现 但是图片没办法序列化
#         items = []
#         for goods in all_goods:
#             item = dict()
#             item['name'] = goods.name
#             item['market_price'] = goods.market_price
#             item['goods_front_image'] = goods.goods_front_image
#             items.append(item)
#         # 使用HttpResponse返回需要先把python的json格式类型转化为json的字符串, 然后加上 content_type
#         # data = json.dumps(items, ensure_ascii=False)  # ensure_ascii=False 为的显示中文
#         # return HttpResponse(data, content_type='application/json')
#         # 使用JsonResponse 返回数据
#         return JsonResponse(items, safe=False)

# class GoodsView(View):
#     def get(self, request):
#         all_goods = Goods.objects.all()  # query list
#         # 第二种序列化 model_to_dict(没办法部分序列化同时图片也没办法序列化)
#         items = []
#         for goods in all_goods:
#             item = model_to_dict(goods)
#             items.append(item)
#         return JsonResponse(items, safe=False)

# class GoodsView(View):
#     def get(self, request):
#         all_goods = Goods.objects.all()  # query list
#         # 第三种序列化 serializers 序列化完是 json 字符串  完美解决了图片序列化问题
#         data_str = serializers.serialize('json', all_goods)
#         data = json.loads(data_str)
#         return JsonResponse(data, safe=False)

# # rest framework 最简单的APIview
# class GoodsView(APIView):
#     def get(self, request):  # 此时的request 已经被 rest framework 封装了
#         all_goods = Goods.objects.all()  # query list
#         serializer = GoodsSerializer(all_goods, many=True)  # 返回的是序列化器
#         return Response(data=serializer.data, status=status.HTTP_200_OK)

# 自定义分页类
class GoodsPagination(pagination.PageNumberPagination):
    page_size = 12
    max_page_size = 100
    page_query_param = 'page'  # 路径参数
    page_size_query_param = 'page_size'  # 允许路径传参 即允许修改每页显示的数量


# class GoodsView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):  # 只需配置
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)  # 配置过滤器
#     # filter_fields = ('name', )   # 根据哪个字段查询 达不到 模糊/区间 需要自定义
#     filter_class = GoodsFilter
#     search_fields = ('name', 'desc', 'goods_brief')
#     ordering_fields = ('shop_price', 'market_price')
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)  # 把过滤/分页全都写好 只需要配置相关过滤器
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)  # 创建一个对象，即post请求


class GoodsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):  # 只需配置
    """
        商品列表接口 带过滤/搜索/分页  以及单个商品即详情
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)  # 配置过滤器
    filter_class = GoodsFilter
    search_fields = ('name', 'desc', 'goods_brief')
    ordering_fields = ('shop_price', 'market_price')
    logging.info(f'gulishop goods list view len queryset {len(queryset)} CUR_ENV:{CUR_ENV}')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer
    logging.info(f'gulishop categorys list view len queryset CUR_ENV:{CUR_ENV}')

    def get_queryset(self):  # 这个self的作用目的是要拿到 登陆的用户
        return GoodsCategory.objects.filter(category_type=1)


# 首页 轮播图 cbv
class IndexBannersViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Banner.objects.all().order_by('-index')
    serializer_class = IndexBannerSerializer
