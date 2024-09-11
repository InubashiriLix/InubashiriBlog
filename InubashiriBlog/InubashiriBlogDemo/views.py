#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName    :views.py
# @Time        :2024/9/10 下午8:53
# @Author      :InubashiriLix

from snakes.get_base_context import get_base_context
from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_GET


@require_GET
def index(request):
    context = get_base_context(request)
    return render(request, 'index.html', context)