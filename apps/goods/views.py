from django.shortcuts import render, HttpResponse
from django.views import View
from .models import Goods
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from rest_framework.views import APIView
from .serializers import GoodsSerializer
from rest_framework.response import Response
from rest_framework import status


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

# rest framework view
class GoodsView(APIView):
    def get(self, request):  # 此时的request 已经被 rest framework 封装了
        all_goods = Goods.objects.all()  # query list
        serializer = GoodsSerializer(all_goods, many=True)  # 返回的是序列化器
        return Response(data=serializer.data, status=status.HTTP_200_OK)
