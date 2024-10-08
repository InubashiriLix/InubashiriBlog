"""InubashiriBlogDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import include
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

from .views import index


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # 国际化配置
]

# 国际化路由
urlpatterns += i18n_patterns(
    path(_(""), index, name="index"),
    path(_('admin/'), admin.site.urls),
    path(_("blog/"), include("blog.urls", namespace='blog')),
    path(_("auth/"), include("blog_auth.urls", namespace="blog_auth")),
)

# 媒体文件处理 (确保在开发环境中能够正确访问媒体文件)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
