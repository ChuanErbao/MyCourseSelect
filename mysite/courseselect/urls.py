from django.conf.urls import url
from . import views

app_name = 'courseselect'

urlpatterns = [
    url(r'^$', views.login, name='index'),
    url('logout', views.logout, name='logout'),
    url('student/index', views.stu_index, name='stu_index'),
    url('student/courseResult.html', views.selected, name='selected'),
    url('student/courseOnline', views.course_select, name='select'),
    url('student/schdule', views.get_schedule, name='schedule'),
    url(r'^student/setnodegree/(?P<s_id>[0-9]+)/(?P<c_id>\d+)/', views.set_no_degree, name='setnodegree'),
    url(r'^student/setdegree/(?P<s_id>[0-9]+)/(?P<c_id>\d+)/', views.set_degree, name='setdegree'),
    url(r'^student/drop/(?P<s_id>[0-9]+)/(?P<c_id>\d+)/', views.drop_course, name='dropcourse'),
    url(r'^student/get/(?P<s_id>[0-9]+)/(?P<c_id>\d+)/', views.get_course, name='getcourse'),

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