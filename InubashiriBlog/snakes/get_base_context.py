#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName    :get_base_context.py
# @Time        :2024/9/10 下午10:46
# @Author      :InubashiriLix
from blog_auth.models import AvatarModel
from django.conf import settings


def get_base_context(request) -> dict:
    user = request.user
    if user.is_authenticated:
        avatar = AvatarModel.objects.filter(user=user).last()
        if avatar:
            return {"avatar": settings.MEDIA_URL + avatar.image.name}  # 确保返回正确的 MEDIA URL
        else:
            return {"avatar": None}
    else:
        return {"avatar": None}