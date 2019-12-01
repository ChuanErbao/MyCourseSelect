from django.conf.urls import url
from . import views

app_name = 'courseselect'

urlpatterns = [
    url(r'^$', views.login, name='index'),
    url('logout', views.logout, name='logout'),
    url('student/index', views.stu_index, name='stu_index'),
    url('student/courseResult.html', views.selected, name='selected'),
    url('student/courseOnline', views.course_select, name='select'),
    url(r'student/predropxk/(?P<s_id>[0-9]+)/(?P<c_id>\d+)/', views.drop_pre_xk, name='dropprexk'),
    url('student/schdule', views.get_schedule, name='schedule'),
    url('student/grade', views.grade, name='grade'),
    url(r'^student/setnodegree/(?P<s_id>[0-9]+)/(?P<c_id>\d+)/', views.set_no_degree, name='setnodegree'),
    url(r'^student/setdegree/(?P<s_id>[0-9]+)/(?P<c_id>\d+)/', views.set_degree, name='setdegree'),
    url(r'^student/drop/(?P<s_id>[0-9]+)/(?P<c_id>\d+)/', views.drop_course, name='dropcourse'),
    url(r'^student/get/(?P<s_id>[0-9]+)/(?P<c_id>\d+)/', views.get_course, name='getcourse'),
    url(r'student/courseLoved', views.pre_selected, name='preselected'),
    url(r'student/preget/(?P<s_id>[0-9]+)/(?P<c_id>\d+)/', views.get_pre, name='getpre'),
    url(r'student/predrop/(?P<s_id>[0-9]+)/(?P<c_id>\d+)/', views.drop_pre, name='droppre'),
    url(r'student/getcoursepre/(?P<s_id>[0-9]+)/(?P<c_id>\d+)/', views.get_course_pre, name='getcoursepre'),

    url('teacher/downloadFile', views.tea_download_file, name='tea_download_file'),
    url('teacher/courseAnnunciate', views.tea_courseAnnunciate, name='tea_courseAnnunciate'),
    url('teacher/courseResult', views.tea_courseResult, name='tea_courseResult'),
    url('teacher/mySchedule', views.tea_mySchedule, name='tea_mySchedule'),
    url('teacher/courseScore', views.tea_courseScore, name='tea_courseScore'),
    url('teacher/getStuMsg', views.tea_getStuMsg, name='tea_getStuMsg'),
    url('teacher/uploadScore', views.tea_uploadScore, name='tea_uploadScore'),
]