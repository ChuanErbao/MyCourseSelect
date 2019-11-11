from django.conf.urls import url
from . import views

app_name = 'courseselect'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^student/(?P<pk>[0-9]+)/index', views.stu_index, name='stu_index'),
    url(r'^student/(?P<pk>[0-9]+)/selected', views.selected, name='selected'),
    
    url('/teacher/courseAnnunciate', views.tea_courseAnnunciate, name='tea_courseAnnunciate'),
    url('/teacher/courseDelete', views.tea_courseDelete, name='tea_courseDelete'),
    url('/teacher/courseResult', views.tea_courseResult, name='tea_courseResult'),
    url('/teacher/mySchedule', views.tea_mySchedule, name='tea_mySchedule'),
    url('/teacher/peopleList', views.tea_peopleList, name='tea_peopleList'),
]