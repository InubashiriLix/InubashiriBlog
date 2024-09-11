#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName    :forms.py
# @Time        :2024/9/6 下午12:52
# @Author      :InubashiriLix

from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel


User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=2, error_messages={
        'required': 'enter username',
        'max_length': 'username length should between 2~20',
    })
    email = forms.EmailField(error_messages={"required": "require email", 'invalid': "invalid email format"})
    captcha = forms.CharField(max_length=6, min_length=6, error_messages={'required': 'require captcha',
                                                                          'invalid': 'invalid verification code'})
    password = forms.CharField(max_length=50, min_length=6, error_messages={'required': 'require password',
                                                                            'min_length': 'pw should be more than 6',
                                                                            'max_length': 'pw should no more than 50'})

    def clean_email(self) -> str:
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('Email has been registered')
        else:
            return email

    def clean_captcha(self) -> str | None:
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError('Wrong Verification Code or Email has been used!')
        else:
            captcha_model.delete()
            return captcha


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={"required": "require email", 'invalid': "invalid email format"})
    password = forms.CharField(min_length=6, max_length=50, error_messages={'required': 'require password'})
    remember = forms.IntegerField(required=False)


class AvatarForm(forms.Form):
    avatar_file = forms.ImageField()
