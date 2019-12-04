"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
# from captcha import views

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'', include('courseselect.urls')),
    url(r'userlogin/', include('userlogin.urls')),
    url(r'^captcha/', include('captcha.urls')),
    # url('refresh_captcha/', views.captcha_refresh),    # 刷新验证码，ajax
]
