# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/7 9:04 下午
@Author ： guos
@File   ：serializers.py
@IDE    ：PyCharm

"""
from rest_framework import serializers
from .models import Goods, GoodsCategory, GoodsImage, Banner


# class GoodsSerializer(serializers.Serializer):
#     # 这里是为了序列化models 的每一个字段，必须保持一致  可以一个一个的序列话
#     name = serializers.CharField(required=True, max_length=30, min_length=3, help_text='名字验证')
#     goods_front_image = serializers.ImageField(required=True)
#     shop_price = serializers.FloatField(required=True)
#     add_time = serializers.DateTimeField(required=True)

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):  # 最后我们用的都是这个方法
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        # fields = ['name', 'add_time']  # 可以选择要序列化的字段
        fields = '__all__'  # 序列化所有字段


class CategorySerializer3(serializers.ModelSerializer):  # 商品类别过滤器类
    # related_name 很重要
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):  # 商品类别过滤器类
    # related_name 很重要
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):  # 商品类别过滤器类
    # related_name 很重要
    sub_cat = CategorySerializer2(many=True)  # 序列化的嵌套

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class IndexBannerSerializer(serializers.ModelSerializer):
    # 首页轮播图 序列化器
    class Meta:
        model = Banner
        fields = '__all__'
