#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName    :forms.py
# @Time        :2024/9/6 下午11:39
# @Author      :InubashiriLix

from django import forms
from .models import BlogCategory


class PubBlogForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=2)
    description = forms.CharField(max_length=268)
    content = forms.CharField(min_length=2, widget=forms.Textarea)
    category = forms.IntegerField()
