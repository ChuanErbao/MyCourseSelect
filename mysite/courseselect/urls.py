from django.conf.urls import url
from . import views

app_name = 'courseselect'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^courses/', views.courses, name='course'),
]