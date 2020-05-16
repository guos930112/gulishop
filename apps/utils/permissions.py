# -*- coding: utf-8 -*-
"""
@Time   ： 2020/5/16 11:25 上午
@Author ： guos
@File   ：permissions.py
@IDE    ：PyCharm

"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # obj -> 即 要操作的 model（数据表） 对象
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        # 是否是本人在操作 owner
        return obj.user == request.user
