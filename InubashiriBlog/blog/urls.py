#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName    :urls.py
# @Time        :2024/9/3 下午5:04
# @Author      :InubashiriLix

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('index', views.index, name='index'),
    path('detail/<int:blog_id>', views.detail_blog, name='blog_detail'),
    path('pub', views.pub_blog, name='pub_blog'),
    path('comment/pub', views.pub_comment, name='pub_comment'),
    path('search', views.search_blog, name='search_blog'),
]