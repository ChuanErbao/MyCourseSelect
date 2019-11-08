from django.conf.urls import url
from . import views

app_name = 'user_login'

urlpatterns = [
    url(r'^$', views.login, name='login'), 
    url('login_check/',views.login_check,name='login_check'),
    url(r'forget_password/',views.forgetpassword,name='forget_password')
]