from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import UserForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import os
import csv
import xlwt
from django.http import JsonResponse
import xlrd
from django.http import FileResponse 
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

# def index(request):
#     return redirect('user_login:login')

def login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            u_id = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            kind = form.cleaned_data['kind']
            request.session['id'] = u_id
            try:
                user = User.objects.get(pk=u_id)
            except:
                return HttpResponse('用户不存在！')
            if user.kind != kind:
                return HttpResponse('请选择正确的用户类型！')
            else:
                if user.password != pwd:
                    return HttpResponse('用户名或密码错误！')
                else:
                    request.session['is_login'] = True
                    if kind == 'student':
                        stu = get_object_or_404(Student, s_id=u_id)
                        context = {'name': stu.name}
                        return redirect('courseselect:stu_index')
                    else:
                        tea = get_object_or_404(Teacher, t_id=u_id)
                        context = {'name': tea.name}
                        return render(request, 'teacher/courseAnnunciate.html', context=context)
    else:
        form = UserForm()
    return render(request, 'courseselect/index.html', context={'form': form})


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect('courseselect:index')
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('courseselect:index')


# 学生模块
# 学生主页 主欢迎加边栏功能（选课，已选课程，成绩查询）
def stu_index(request):
    # 先检测登录没有，没有的话就重定向到登陆页面
    if request.session['is_login'] is not True:
        return redirect('courseselect:index')
    else:
        pk = request.session['id']
        stu = get_object_or_404(Student, s_id=pk)
        name = stu.name
        s_id = stu.s_id
        time = StartDate.objects.all()[0]
        context = {
            'name': name,
            'id': s_id,
            'time': time
        }
        return render(request, 'student/courseAnnunciate.html', context=context)


# 查看已选择的课程
def selected(request):
    if request.session.get('is_login') is None:
        redirect('courseselect:index')
    else:
        pk = request.session['id']
        courses = StudentCourse.objects.filter(student=Student.objects.get(s_id=pk))
        stu = get_object_or_404(Student, s_id=pk)
        total_credit = 0
        degree_credit = 0
        courses_info = []
        for c in courses:
            if c.attribute == 'is':
                degree_credit += c.course.credit
            total_credit += c.course.credit
            course_info = c.course
            courses_info.append([course_info, c.attribute])
        name = stu.name
        s_id = stu.s_id
        context = {
            'courses': courses_info,
            'stu': stu,
            'id': s_id,
            'total_credit': total_credit,
            'degree_credit': degree_credit,
        }
        return render(request, 'student/courseResult.html', context=context)


# 进入选课页面
# 选课页面首先要把所有的课程都列出来，然后选择、提交表单
# 判断是否选课冲突
def allow(course, courses):
    sw = course.start_week
    ew = course.end_week
    tm = course.arr_course
    for c in courses:
        if c.start_week < ew or c.end_week > sw:
            if tm == c.arr_course:
                return False
    return True


def course_select(request):
    # 首先判断课程选满没有，是否与学生课程冲突
    # 若不满足，直接回来，然后提示框告诉他为啥
    # 若满足，课程的选课人数加一，学生已选课程增加上， 课程已选学生加上
    if request.method == "POST":
        stu_id = request.session['id']
        course_id = request.POST.get('course_id')
        course = Course.objects.get(pk=course_id)
        courses = StudentCourse.objects.filter(pk=id)
        # 判断是否冲突,以及人数是否达到上限
        if course.selected_now < course.selected_limit and allow():
            sc = StudentCourse.objects.create(student_id=stu_id, course_id=course_id)
            course.selected_now += 1
            sc.save()
            return render(request, 'student/course_select.html')
# 只显示未选课程
# 实现分页功能
    else:
        if request.session.get('is_login', None) is None:
            return redirect('courseselect:index')
        pk = request.session['id']
        stu = get_object_or_404(Student, s_id=pk)
        selected_courses = StudentCourse.objects.filter(student=Student.objects.get(s_id=pk))
        courses = Course.objects.all()
        for sc in selected_courses:
            if sc.course in courses:
                courses = courses.exclude(c_id=sc.course.c_id)
        paginator = Paginator(courses, 2)
        page = request.GET.get('page')
        courses = paginator.get_page(page)
        context = {'courses': courses, 'name': stu.name, 'selected_courses': selected_courses, }
        return render(request, 'student/courseOnline.html', context=context)


# 成绩查询
def grade(request):
    pass


# 查看课表并下载
def get_schedule(request):
    if request.session.get('is_login') is not True:
        redirect('courseselect:index')
    stu = get_object_or_404(Student, s_id=request.session['id'])
    context = {
        'name': stu.name,
    }
    return render(request, 'student/mySchedule.html', context=context)


# 设为非学位课
def set_no_degree(request, s_id, c_id):
    c = StudentCourse.objects.get(student=Student.objects.get(s_id=s_id), course=Course.objects.get(c_id=c_id))
    c.attribute = 'not'
    c.save()
    return redirect(reverse('courseselect:selected'))

# 设为非学位课
def set_degree(request, s_id, c_id):
    c = StudentCourse.objects.get(student=Student.objects.get(s_id=s_id), course=Course.objects.get(c_id=c_id))
    c.attribute = 'is'
    c.save()
    return redirect(reverse('courseselect:selected'))


# 退选
def drop_course(request, s_id, c_id):
    c = StudentCourse.objects.get(student=Student.objects.get(s_id=s_id), course=Course.objects.get(c_id=c_id))
    c.delete()
    return redirect(reverse('courseselect:selected'))

# 教师模块------------------------------------------------以下已经改动-----------------------------

# 选课公告
def tea_courseAnnunciate(request):
    return render(request,'teacher/courseAnnunciate.html') 

# 退课情况
def tea_courseDelete(request):
    return render(request,'teacher/courseDelete.html') 

# 选课结果
def tea_courseResult(request):
    context= {}
    context['isadmin'] = 1
    list=[]
    list.append({"id":1,"course_no":"20190128121","subject_name":"数学"
        ,"credit":3,"place":"教学楼一","start_week":2,"end_week":18,
        "course_section":"1,2","course_weekday":"3","check_people":"100","people_max":"120"}) 
    context['list'] = list
    return render(request,'teacher/courseResult.html',context) 

# 教师课表
def tea_mySchedule(request):
    context= {}
    courses=[]
    week_course=["数学","","","","","",""]
    courses.append(week_course)
    week_course=["","","","","","英语",""]
    courses.append(week_course)
    week_course=["","","","","","",""]
    courses.append(week_course)
    week_course=["","","","","","",""]
    courses.append(week_course)
    week_course=["数学","","","","","",""]
    courses.append(week_course)
    week_course=["","","","","","英语",""]
    courses.append(week_course)
    week_course=["数学","","","","","",""]
    courses.append(week_course)
    context["courses"]=courses
    return render(request,'teacher/mySchedule.html',context) 

# 
# def tea_peopleList(request):
#     return render(request,'teacher/peopleList.html') 

# 选课成绩录入界面
def tea_courseScore(request):
    context= {}
    list=[]
    student={"stu_name":"王化磊","stu_no":"1201","stu_academy":"计算机学院"}
    students=[student,student,student,student,student,student,student,student,student,student,student,student,student,student,student]
    list.append({"course_name":"数学课","course_no":"20190101","students":students}) 
    student={"stu_name":"王珊珊","stu_no":"1202","stu_academy":"会计学院"}
    students=[student,student,student,student,student,student,student,student]
    list.append({"course_name":"会计科","course_no":"20190102","students":students}) 
    context['course_all'] = list
    return render(request,'teacher/courseScore.html',context)

# def tea_setScore(request):
#     # 获取浏览器传来的信息-学生学号，课程号，分数 
#     return render(request,'teacher/courseScore.html')

# 返回录入课程成绩模板
def tea_download_file(request):
    # 获取教师编号，课程编号
    course_no=api=request.GET.get("course_no")
    # 根据课程编号获取数据库中的学生选课数据
    # 根据数据生成相应的文件（学生学号，学生姓名，成绩（空）），并保存文件
    # 将保存的文件返回，即该文件就是用户需要下载的登录成绩的模板文件

    curPath = os.path.abspath(os.path.dirname(__file__)) 
    filename='2019121_course.xls'
    file = "templates/"+filename 
    filepath = os.path.join(curPath, file)   

    # 因为输入都是Unicode字符，这里使用utf-8，免得来回转换
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

    booksheet.write(0, 0, "学号")
    booksheet.write(0, 1, "姓名")
    booksheet.write(0, 2, "成绩")

    for i in range(1,100):
        booksheet.write(i, 0, "21212121")
        booksheet.write(i, 1, "王化磊")
        booksheet.write(i, 2, "")  

    # 保存文件
    workbook.save(filepath)

    fp = open(filepath, 'rb')
    response =FileResponse(fp)  
    response['Content-Type']='application/octet-stream'  
    response['Content-Disposition']='attachment;filename="'+filename+'"'
    print('attachment;filename='+'"'+filename+'"')
    print(response['Content-Disposition'])
    return response
    fp.close() 

# 根据教师上传的课程成绩表将成绩录入数据库
@csrf_exempt
def tea_uploadScore(request):
    # 1 获取前端传输的文件对象,并将其写入内存
    file_obj = request.FILES.get('file')  
    print(request.POST.get('course_no'))
    file="templates/"+file_obj.name
    curPath = os.path.abspath(os.path.dirname(__file__)) 
    path = os.path.join(curPath, file)
    fp = open(path, 'wb+')
    # chunks将对应的文件数据转换成若干片段, 分段写入, 可以有效提 高文件的写入速度, 适用于2.5M以上的文件
    for chunk in file_obj.chunks():
        fp.write(chunk)
    fp.close() 

    # 2 读取写入的文件，解析、判断、写入数据库 
    
    # 2.1 获取工作表list。
    mySheets = xlrd.open_workbook(path).sheets()             
    # 2.2 通过索引顺序获取。    
    mySheet = mySheets[0]
    # 2.3 获取行数与列数 
    nrows = mySheet.nrows
    ncols = mySheet.ncols
 
    for row in range(0,nrows-1):
        for col in range(0,ncols-1):
            myCell = mySheet.cell_value(row, col) 
            print(myCell)

    # 给服务器返回信息
    response={}
    response['msg']="操作成功"
    return JsonResponse(response)


# 获取课程对应的选课学生信息
def tea_getStuMsg(request):
    # 1 获取课程编号
    course_no=request.GET.get("course_no")
    # 2 根据课程编号获取对应课程的学生信息

    # 3 将学生信息写入文件
    curPath = os.path.abspath(os.path.dirname(__file__)) 
    filename=course_no+'_course_stuMsg.xls'
    file = "templates/"+filename 
    filepath = os.path.join(curPath, file)   

    # 因为输入都是Unicode字符，这里使用utf-8，免得来回转换
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

    booksheet.write(0, 0, "学号")
    booksheet.write(0, 1, "姓名") 

    for i in range(1,100):
        booksheet.write(i, 0, "21212121")
        booksheet.write(i, 1, "王化磊") 

    # 保存文件
    workbook.save(filepath)

    # 4将文件返回给请求源

    fp = open(filepath, 'rb')
    response =FileResponse(fp)  
    response['Content-Type']='application/octet-stream'  
    response['Content-Disposition']='attachment;filename="'+filename+'"'
    # print('attachment;filename='+'"'+filename+'"')
    # print(response['Content-Disposition'])
    return response
    fp.close() 