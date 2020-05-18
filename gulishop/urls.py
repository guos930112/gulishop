"""gulishop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
import xadmin

from django.views.static import serve
from gulishop.settings import MEDIA_ROOT
# from goods.views import GoodsView
from goods.views import GoodsViewSet, CategoryViewSet
from users.views import VerifyCodeViewSet, UserViewSet
from operations.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddressViewSet
from trade.views import ShopCartViewSet, OrderInfoViewSet, AliPayView

from rest_framework import routers
from django.views.generic import TemplateView
router = routers.DefaultRouter()
router.register(r'goods', GoodsViewSet, basename='goods')   # 这里就是接口定义的位置
router.register(r'categorys', CategoryViewSet, basename='categorys')
router.register(r'code', VerifyCodeViewSet, basename='code')
router.register(r'users', UserViewSet, basename='users')
router.register(r'userfavs', UserFavViewSet, basename='userfavs')
router.register(r'messages', UserLeavingMessageViewSet, basename='messages')
router.register(r'address', UserAddressViewSet, basename='address')
router.register(r'shopcarts', ShopCartViewSet, basename='shopcarts')
router.register(r'orders', OrderInfoViewSet, basename='orders')

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    url(r'^ueditor/', include('DjangoUeditor.urls')),

    # url(r'^goods/$', GoodsView.as_view()),
    # url(r'^goods/$', GoodsView.as_view({'get': 'list'})),
    url(r'^api-auth/', include('rest_framework.urls')),  # browser api 的登陆/退出
    url(r'', include(router.urls)),
    # # 这是token 登陆-认证方式
    # url(r'^login/', views.obtain_auth_token),  # 这里已经把login的post请求给我们做了
    # 这是JWT Token 登陆-认证方式
    url(r'^login/', obtain_jwt_token),
    url(r'^alipay_return/$', AliPayView.as_view(), name='alipay'),
    url(r'^index/$', TemplateView.as_view(template_name='index.html'), name='index'),

]
