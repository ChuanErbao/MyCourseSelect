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


# 教师模块
# 教师主页，样子和学生一样，侧栏功能（查看已开设课程， 打分， 增加课程人数上限并添加学生，查看已选课学生并打印名单）
def tea_index(request, pk):
    tea = get_object_or_404(Teacher, pk=pk)
    t_id = tea.t_id
    name = tea.name
    context = {
        'name': name
    }
    return render(request, 'teacher/index.html', context=context)


# 打分，使用导入成绩的方法，不然逐个填太麻烦了
def add_score(request):
    pass


# 添加学生，如果教师要添加学生，先判断人数是否满了，只有满了才能加学生
# 以提交表单的方式提交学号，post的值就是学号，然后通过这个学号给学生加课程、给课程加学生、同时课程人数加一
def add_extra_stu(request):
    pass


# 进入该课程查看学生信息及成绩
def lookup(request):
    pass
