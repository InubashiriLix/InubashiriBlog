import string
import random
import os
from dotenv import load_dotenv

from django.db import connection

from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.core.mail import send_mail
# models and forms
from .models import CaptchaModel, AvatarModel
from blog.models import Blog
from .forms import RegisterForm, LoginForm, AvatarForm
from django.contrib.auth import get_user_model, login, logout
# customized functions / classes
from .EmailSender import send_verification_email_async
from snakes.get_base_context import get_base_context

User = get_user_model()

load_dotenv()



@require_http_methods(['POST', 'GET'])
def blog_login(request):
    base_context = get_base_context(request=request)
    if request.method == 'GET':
        return render(request, 'login.html', context=base_context)
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(raw_password=password):
                # user.is_authenticated =
                login(request, user)
                if not remember:
                    # if remember is not checked:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(2_592_000)
                return redirect(reverse('blog:index'))
            else:
                # print('login: Failed!')
                form.add_error('email', 'email or password wrong')
                form.add_error('password', 'Or this email has not be registered')
                return render(request, 'login.html', context=base_context | {"form": form})  # the dict | operation start from 3.9!
        else:
            return render(request, 'login.html', context=base_context | {"form": form})


@require_http_methods(['POST', 'GET'])
def register(request):
    base_context = get_base_context(request=request)
    if request.method == 'GET':
        return render(request, 'register.html', context=base_context)
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)  # password will be encoded in the method
            return redirect(reverse('blog_auth:login'))
        else:
            print(form.errors)
            form.add_error('username', 'register failed, check your info')
            return render(request, 'register.html', context=base_context | {"form": form})


@login_required()  # it  must be login state so no more validations are needed
@require_http_methods(["GET", "POST"])
def get_profile_page(request):
    # TODO: we need
    base_context = get_base_context(request=request)
    user = request.user
    if request.method == "GET":
        blogs = Blog.objects.filter(author_id=user.id).all()
        context_blog = {"blogs": blogs} if blogs else {"blogs": None}
        # print("FUCK")
        # for blog in blogs:
        #     print(blog.id)
        return render(request, 'profile.html', context=base_context | context_blog)
    else:  # POST
        form = AvatarForm(request.POST, files=request.FILES)
        if form.is_valid():

            # create new avatar model
            avatar = form.cleaned_data.get('avatar_file')
            avatar_obj = AvatarModel.objects.create(image=avatar, user=user)

            # bind the avatar to user
            with connection.cursor() as cursor:
                cursor.execute("UPDATE auth_user SET avatar_id = %s WHERE id = %s", [avatar_obj.id, user.id])
            # TODO: MAY BE YOU CAN CREATE A NEW USER CLASS AND ADD THE PREVIOUS LIST (MODEL LAYER USER CLASS "auth_user")
            user.save()

            return redirect(reverse('blog_auth:profile'))
        else:
            print(form.errors)
            return render(request, 'profile.html', context=base_context | {"form": form, "user": user})



def _generate_captcha_in_model(email: str) -> str:
    captcha = ''.join(random.sample(string.digits, k=6))
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    return captcha


def send_email_captcha(request):
    # get email info
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'msg': 'the email cannot be empty'})

    # generate verification code (6 digits)
    captcha = _generate_captcha_in_model(email=email)

    # the sender selection
    USE_DJANGO_BUILTIN_EMAIL_SENDER = os.getenv('USE_DJANGO_EMAIL_SENDER_IN_AUTH_REGISTER') == "1"

    if USE_DJANGO_BUILTIN_EMAIL_SENDER:
        try:
            print('using builtin sender')
            SENDER_EMAIL = os.getenv('SENDER_EMAIL')
            send_mail(subject='【 Verification 】 InubashiriLix Blog Verification',
                      message=f'you\'re registering InubashiriLix blog, and vertification code is {captcha}',
                      from_email=SENDER_EMAIL,
                      recipient_list=[email],
                      fail_silently=False)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 500, 'msg': 'email sending failed'})
    else:
        print('using customized sender')
        if send_verification_email_async(email, captcha):
            return JsonResponse({"code": 200, "message": "register verification has been sent"})
        else:
            return JsonResponse({"code": 500, "message": "email sending failed"})


def auth_logout(request):
    logout(request)
    return redirect(reverse('blog:index'))

