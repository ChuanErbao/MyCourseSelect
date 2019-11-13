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
def stu_index(request):
    # 先检测登录没有，没有的话就重定向到登陆页面
    if request.session['is_login'] is True:
        redirect('login.html')
    else:
        pk = request.session['id']
        stu = get_object_or_404(Student, pk=pk)
        name = stu.name
        s_id = stu.s_id
        context = {
            'name': name,
            'id': s_id,
        }
        return render(request, 'student/stu_index.html', context=context)


# 查看已选择的课程
def selected(request):
    if request.session['is_login'] is True:
        redirect('login.html')
    else:
        pk = request.session['id']
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
# 选课页面首先要把所有的课程都列出来，然后选择、提交表单
def course_select(request):
    # 首先判断课程选满没有，是否与学生课程冲突
    # 若不满足，直接回来，然后提示框告诉他为啥
    # 若满足，课程的选课人数加一，学生已选课程增加上， 课程已选学生加上
    if request.method == "POST":
        stu_id = request.session['id']
        course_id = request.POST.get('course_id')
        course = Course.objects.get(pk=course_id)
        # 判断是否冲突,以及人数是否达到上限
        if course.selected_now  < course.selected_limit:
            sc = StudentCourse.objects.create(student_id=stu_id, course_id=course_id)
            course.selected_now += 1
            sc.save()
            redirect('')
# 只显示未选课程
    else:
        pk = request.session['id']
        selected_courses = StudentCourse.objects.filter(pk=pk)
        courses = Course.objects.all()
        for sc in selected_courses:
            if sc in courses:
                courses.pop(sc)
        context = {'courses': courses}
        return render(request, 'student/course_select.html', context=context)


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

def tea_courseScore(request):
    context= {}
    list=[]
    student={"stu_name":"王化磊","stu_no":"1201","stu_academy":"计算机学院"}
    students=[student,student,student,student,student,student,student,student]
    list.append({"course_name":"数学课","course_id":"collapse_1","students":students}) 
    student={"stu_name":"王珊珊","stu_no":"1202","stu_academy":"会计学院"}
    students=[student,student,student,student,student,student,student,student]
    list.append({"course_name":"会计科","course_id":"collapse_2","students":students}) 
    context['course_all'] = list
    return render(request,'teacher/courseScore.html',context)

