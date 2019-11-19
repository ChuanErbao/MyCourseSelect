from django.conf.urls import url
from . import views

app_name = 'courseselect'

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url('course_select/index', views.stu_index, name='stu_index'),
    url('course_select/courseResult.html', views.selected, name='selected'),
    
    url('teacher/downloadFile', views.tea_download_file, name='tea_download_file'),
    url('teacher/courseAnnunciate', views.tea_courseAnnunciate, name='tea_courseAnnunciate'),
    url('teacher/courseDelete', views.tea_courseDelete, name='tea_courseDelete'),
    url('teacher/courseResult', views.tea_courseResult, name='tea_courseResult'),
    url('teacher/mySchedule', views.tea_mySchedule, name='tea_mySchedule'),
    # url('teacher/peopleList', views.tea_peopleList, name='tea_peopleList'),
    url('teacher/courseScore', views.tea_courseScore, name='tea_courseScore'),
    # url('teacher/setScore', views.tea_setScore, name='tea_setScore'),
    url('teacher/getStuMsg', views.tea_getStuMsg, name='tea_getStuMsg'),
    url('teacher/uploadScore', views.tea_uploadScore, name='tea_uploadScore'),
]