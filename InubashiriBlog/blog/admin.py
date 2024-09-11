#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName    :blog.py
# @Time        :2024/9/6 下午9:59
# @Author      :InubashiriLix
from django.contrib import admin
from .models import BlogCategory, Blog, BlogComment


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'pub_time', 'category', 'author']


class BlogDescriptionAdmin(admin.ModelAdmin):
    list_display = ['content', 'blog']


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'pub_time', 'author', 'blog']


admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
