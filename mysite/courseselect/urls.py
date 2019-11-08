from django.conf.urls import url
from . import views

app_name = 'courseselect'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^student/(?P<pk>[0-9]+)/index', views.stu_index, name='stu_index'),
    url(r'^teacher/(?P<pk>[0-9]+)/index', views.tea_index, name='tea_index'),
]