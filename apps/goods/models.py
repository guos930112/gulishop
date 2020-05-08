from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField


# Create your models here.


class GoodsCategory(models.Model):
    """
        商品类别信息表
    """
    name = models.CharField(max_length=20, verbose_name='商品类别名称')
    category_type = models.IntegerField(choices=((1, '一级'), (2, '二级'), (3, '三级')), verbose_name='类别级别')
    code = models.CharField(max_length=50, verbose_name='类别编号')
    parent_category = models.ForeignKey('self', verbose_name='所属上级类别', null=True, blank=True,
                                        related_name='sub_cat', on_delete=models.CASCADE)  # 自关联 类似省市区 一张表搞定不用分表，因为字段都一样
    is_tab = models.BooleanField(default=False, verbose_name='是否导航')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品类别信息'
        verbose_name_plural = verbose_name


class Goods(models.Model):
    """
        商品信息表
    """
    category = models.ForeignKey(GoodsCategory, verbose_name='所属类别', related_name='goods', on_delete=models.CASCADE)  # 外键 和商品类别关联
    name = models.CharField(max_length=100, verbose_name='商品名称')
    goods_sn = models.CharField(max_length=30, verbose_name='商品唯一编号', unique=True, null=True, blank=True)
    goods_brief = models.CharField(max_length=300, verbose_name='商品简介', null=True, blank=True)
    desc = UEditorField(verbose_name='商品详情',
                        width=900,
                        height=400,
                        toolbars='full',
                        imagePath='ueditor/images/',
                        filePath='ueditor/files/',
                        upload_settings={'imageMaxSizing': 1024000},
                        default='')
    goods_front_image = models.ImageField(upload_to='goods/images', max_length=200, verbose_name='商品封面图')
    market_price = models.FloatField(verbose_name='商品市场价')
    shop_price = models.FloatField(verbose_name='商品店铺价')
    ship_free = models.BooleanField(default=True, verbose_name='是否包邮')
    click_num = models.IntegerField(default=0, verbose_name='商品访问量')
    fav_num = models.IntegerField(default=0, verbose_name='商品收藏数')
    goods_num = models.IntegerField(default=100, verbose_name='商品库存数')
    sold_num = models.IntegerField(default=0, verbose_name='商品销售数')
    is_hot = models.BooleanField(default=False, verbose_name='是否热卖')
    is_new = models.BooleanField(default=False, verbose_name='是否新品')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name


class CategoryBrand(models.Model):
    """
        赞助商信息表
    """
    category = models.ForeignKey(GoodsCategory, verbose_name='所属类别', related_name='brands', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='brand/images', verbose_name='赞助图片', max_length=200)
    name = models.CharField(max_length=30, verbose_name='赞助名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '赞助信息'
        verbose_name_plural = verbose_name


class GoodsImage(models.Model):
    """
        商品轮播图
    """
    goods = models.ForeignKey(Goods, verbose_name='所属商品', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='goods/images', verbose_name='商品轮播图片', max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = '商品轮播图信息'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    """
        首页轮播图
    """
    goods = models.ForeignKey(Goods, verbose_name='所属商品', related_name='banners', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner/images', verbose_name='首页轮播图片', max_length=200)
    index = models.IntegerField(verbose_name='轮播顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = '首页轮播图信息'
        verbose_name_plural = verbose_name


class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords
