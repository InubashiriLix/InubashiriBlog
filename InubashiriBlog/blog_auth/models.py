from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class CaptchaModel(models.Model):
    email = models.EmailField(unique=True)
    captcha = models.CharField(max_length=6)
    create_time = models.DateTimeField(auto_now_add=True)


class AvatarModel(models.Model):
    image = models.ImageField(upload_to="avatars/")  # 推荐使用此路径，并设置 MEDIA_URL 和 MEDIA_ROOT
    user = models.ForeignKey(User, on_delete=models.CASCADE)


#  TODO : front to go


