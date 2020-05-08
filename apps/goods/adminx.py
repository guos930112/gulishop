# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/6 4:00 下午
@Author ： guos
@File   ：adminx.py
@IDE    ：PyCharm

"""
import xadmin
from .models import *
from xadmin import views


class BaseXadminSetting(object):
    """
        设置后台管理主题类
    """
    enable_themes = True
    use_bootswatch = True


class CommXadminSetting(object):
    """
        设置头部/底部/折叠 信息
    """
    site_title = '谷粒商城后台管理系统'
    site_footer = '小帅工作室'
    menu_style = 'accordion'


class GoodsCategoryAdmin(object):
    """
        商品类别信息表
    """
    list_display = ['name', 'category_type', 'code', 'parent_category', 'is_tab', 'add_time']


class GoodsAdmin(object):
    """
        商品信息表
    """
    list_display = ['category', 'name', 'goods_sn', 'goods_brief', 'click_num', 'fav_num', 'is_hot', 'add_time']
    style_fields = {'desc': 'ueditor'}
    search_fields = ['name', ]
    list_editable = ["is_hot", ]
    list_filter = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                   "shop_price", "is_new", "is_hot", "add_time"]


class CategoryBrandAdmin(object):
    """
        赞助商信息表
    """
    list_display = ['category', 'name', 'image', 'add_time']


class GoodsImageAdmin(object):
    """
        商品轮播图
    """
    list_display = ['goods', 'image', 'add_time']


class BannerAdmin(object):
    """
        首页轮播图
    """
    list_display = ['goods', 'image', 'index', 'add_time']


class HotSearchWordsAdmin(object):
    """
    热搜词
    """
    list_display = ['keywords', 'index', 'add_time']


xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(CategoryBrand, CategoryBrandAdmin)
xadmin.site.register(GoodsImage, GoodsImageAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(HotSearchWords, HotSearchWordsAdmin)
xadmin.site.register(views.BaseAdminView, BaseXadminSetting)
xadmin.site.register(views.CommAdminView, CommXadminSetting)
