from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import HttpResponse
from .models import *

# Create your views here.


# 首页，选择用户类型
def index(request):
    return render(request, 'courseselect/index.html')


# 登录模块
def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        pass


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")


# 学生模块
# 学生主页 主欢迎加边栏功能（选课，已选课程，成绩查询）
def stu_index(request, pk):
    stu = get_object_or_404(Student, pk=pk)
    name = stu.name
    s_id = stu.s_id
    context = {
        'name':name,
        'id':s_id,
    }
    return render(request, 'student/stu_index.html', context=context)


# 查看已选择的课程
def selected(request, pk):
    courses = StudentCourse.objects.filter(student_id=pk)
    stu = get_object_or_404(Student, pk=pk)
    courses_info = []
    for c in courses:
        course_info = get_object_or_404(Course, pk=c.course_id)
        courses_info.append(course_info)
    name = stu.name
    s_id = stu.s_id
    context = {
        'courses': courses_info,
        'name': name,
        'id': s_id,
    }
    return render(request, 'student/selected.html', context=context)


# 进入选课页面
def course_select(request):
    if request.method == "GET":
        return render(request, 'student/course_select.html')


# 首先判断课程选满没有，是否与学生课程冲突
# 若不满足，直接回来，然后提示框告诉他为啥
# 若满足，课程的选课人数加一，学生已选课程增加上， 课程已选学生加上
    if request.method == "POST":
        redirect('')


# 成绩查询
def score(request):
    pass


# 教师模块------------------------------------------------以下已经改动-----------------------------
def tea_courseAnnunciate(request):
    return render(request,'teacher/courseAnnunciate.html') 

def tea_courseDelete(request):
    return render(request,'teacher/courseDelete.html') 

def tea_courseResult(request):
    context= {}
    context['isadmin'] = 1
    list=[]
    list.append({"id":1,"subject_no":"20190128121","subject_name":"数学"
        ,"credit":3,"place":"教学楼一","start_week":2,"end_week":18,
        "course_section":"1,2","course_weekday":"3","check_people":"100","people_max":"120"}) 
    context['list'] = list
    return render(request,'teacher/courseResult.html',context) 

def tea_mySchedule(request):
    return render(request,'teacher/mySchedule.html') 

def tea_peopleList(request):
    return render(request,'teacher/peopleList.html') 