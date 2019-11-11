from django.conf.urls import url
from . import views

app_name = 'user_login'

urlpatterns = [
    url(r'^$', views.login, name='login'), 
    url(r'^login_check',views.login_check,name='login_check'),
    url(r'^forget_password',views.forget_password,name='forget_password'),
    url(r'^do_forget_password',views.forget_password_do,name='forget_password_do')
]