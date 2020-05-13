from django.shortcuts import render
from rest_framework import mixins, viewsets
from .models import UserFav
from .serializers import UserFavSerializer
# Create your views here.


class UserFavViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
