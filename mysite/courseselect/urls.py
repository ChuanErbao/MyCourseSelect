from django.conf.urls import url
from . import views

app_name = 'courseselect'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^student/(?P<pk>[0-9]+)/index', views.stu_index, name='stu_index'),
    url(r'^student/(?P<pk>[0-9]+)/selected', views.selected, name='selected'),
    
    url(r'^/teacher/courseAnnunciate', views.tea_courseAnnunciate, name='tea_courseAnnunciate'),
    url(r'^/teacher/courseDelete', views.tea_courseDelete, name='tea_courseDelete'),
    url(r'^/teacher/courseResult', views.tea_courseResult, name='tea_courseResult'),
    url(r'^/teacher/mySchedule', views.tea_mySchedule, name='tea_mySchedule'),
    url(r'^/teacher/peopleList', views.tea_peopleList, name='tea_peopleList'),
]