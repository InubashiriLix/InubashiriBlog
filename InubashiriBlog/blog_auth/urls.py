#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName    :urls.py
# @Time        :2024/9/4 下午6:01
# @Author      :InubashiriLix

from django.urls import path
from . import views

app_name = 'blog_auth'

urlpatterns = [
    path('login', views.blog_login, name='login'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='email'),
    path('logout', views.auth_logout, name='auth_logout'),
    path('profile', views.get_profile_page, name='profile'),
]