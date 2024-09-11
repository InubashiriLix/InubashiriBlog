from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class BlogCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='category name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('博客分类')
        verbose_name_plural = _('博客分类')


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='title')
    description = models.CharField(max_length=268, verbose_name='description')
    content = models.TextField(verbose_name='content')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='pub_time')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, verbose_name='category')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('博客')
        verbose_name_plural = _('博客')
        ordering = ['-pub_time']


class BlogComment(models.Model):
    content = models.CharField(max_length=1000, verbose_name='content')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='pub_time')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='blog', related_name='comments')
    # you can also use {{ blog.blogcomment_set }} to get all the comment too this blog instead of using related_name
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _('博客评论')
        verbose_name_plural = _('博客评论')
        ordering = ['-pub_time']

