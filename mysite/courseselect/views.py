from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import UserForm, SearchForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import os
import csv
import xlwt
from django.http import JsonResponse
import markdown
import xlrd
from django.http import FileResponse 
from django.views.decorators.csrf import csrf_exempt
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


# Create your views here.

# def index(request):
#     return redirect('user_login:login')

def login(request):
    if request.session.get('is_login', None):
        if request.session['kind'] == 'student':
            return redirect('courseselect:stu_index')
        else:
            return redirect('courseselect:tea_courseAnnunciate')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            u_id = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            kind = form.cleaned_data['kind']
            request.session['id'] = u_id
            request.session['kind'] = kind
            try:
                user = User.objects.get(pk=u_id)
            except:
                response = {}
                response['msg'] = '用户不存在'
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
                        return redirect('courseselect:tea_courseAnnunciate')
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
        now = timezone.now()
        pk = request.session['id']
        stu = get_object_or_404(Student, s_id=pk)
        posts = Post.objects.all()
        name = stu.name
        s_id = stu.s_id
        time = Date.objects.all()[0]
        if now < time.start_time:
            is_start = 0
        else:
            is_start = 1
        context = {
            'name': name,
            'id': s_id,
            'time': time,
            'is_start': is_start,
            'posts': posts,
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


def course_select(request):
    if request.method == "POST":
        s_form = SearchForm(request.POST)
        if s_form.is_valid():
            content = s_form.cleaned_data['content']
            courses = Course.objects.filter(name__contains=content)
    else:
        courses = Course.objects.all()
    if request.session.get('is_login', None) is None:
        return redirect('courseselect:index')
    pk = request.session['id']
    form = SearchForm()
    stu = get_object_or_404(Student, s_id=pk)
    selected_courses = StudentCourse.objects.filter(student=Student.objects.get(s_id=pk))
    loved = []
    for sc in selected_courses:
        if sc.course in courses:
            courses = courses.exclude(c_id=sc.course.c_id)
    courses = sorted(courses, key=lambda course: course.hot_value, reverse=True)

    paginator1 = Paginator(courses, 2)
    page = request.GET.get('page')
    courses = paginator1.get_page(page)
    for c in courses:
        try:
            Pre.objects.get(student=Student.objects.get(s_id=pk), course=c)
            loved.append('1')
        except:
            loved.append('0')
    loved = zip(courses, loved)
    context = {'courses': courses, 'stu': stu, 'selected_courses': selected_courses, 'form': form,'loved': loved }
    return render(request, 'student/courseOnline.html', context=context)


# 成绩查询
def grade(request):
    stu = get_object_or_404(Student, s_id=request.session['id'])
    scs = StudentCourse.objects.filter(student=Student.objects.get(s_id=request.session['id']))
    context = {
        'stu': stu,
        'scs': scs,
    }
    return render(request, 'student/courseAch.html', context=context)


# 查看课表并下载
def get_schedule(request):
    if request.session.get('is_login') is not True:
        redirect('courseselect:index')
    stu = get_object_or_404(Student, s_id=request.session['id'])
    scs = StudentCourse.objects.filter(student=stu)
    courses = []
    for sc in scs:
        courses.append(sc.course)
    context = {
        'name': stu.name,
        'courses': courses,
    }
    courses = sorted(courses, key=lambda course: course.weekdays)
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
    course = Course.objects.get(c_id=c_id)
    c.delete()
    course.selected_now -= 1
    course.save()
    return redirect(reverse('courseselect:selected'))


# 判断是否选课冲突
def allow(course, courses):
    sw = course.start_week
    ew = course.end_week
    wd = course.weekdays
    st = course.start_time
    et = course.end_time
    for c in courses:
        if c.start_week < ew or c.end_week > sw:
            if wd == c.weekdays:
                if c.start_time <  st and c.end_time < st:
                    return True, None
                elif c.start_time > et:
                        return True, None
                else:
                    return False, c
    return True, None


# 判断人数是否满了
def is_full(c_id):
    course = get_object_or_404(Course, c_id=c_id)
    if course.selected_now + 1 <= course.selected_limit:
        return False
    return True


# 选课按钮
def get_course(request, s_id, c_id):
    now = timezone.now()
    date = Date.objects.all()[0]
    if now < date.start_time:
        return HttpResponse("选课尚未开始")
    if now > date.end_time:
        return HttpResponse("选课已经结束")
    full = is_full(c_id)
    courses = []
    aim_course = get_object_or_404(Course, c_id=c_id)
    scs = StudentCourse.objects.filter(student=Student.objects.get(s_id=s_id))
    for sc in scs:
        courses.append(sc.course)
    tag, conflict = allow(aim_course, courses)
    if tag and not full:
        c = StudentCourse(student=Student.objects.get(s_id=s_id), course=Course.objects.get(c_id=c_id))
        c.save()
        aim_course.selected_now += 1
        aim_course.save()
        return redirect(reverse('courseselect:select'))
    elif not tag and not full:
        return HttpResponse("与" + conflict.name + '冲突')
    else:
        return HttpResponse("选课人数已满")


# 正式选课页面取消收藏
def drop_pre_xk(request, s_id, c_id):
    co = Course.objects.get(c_id=c_id)
    cs = Pre.objects.filter(student=Student.objects.get(s_id=s_id), course=co)
    for c in cs:
        c.delete()
    co.hot_value -= 1
    co.save()
    return redirect(reverse('courseselect:select'))


# 预选课界面
def pre_selected(request):
    if request.session.get('is_login') is None:
        redirect('courseselect:index')
    s_id = request.session['id']
    stu = get_object_or_404(Student, s_id=s_id)
    scs = Pre.objects.filter(student=Student.objects.get(s_id=s_id))
    courses = []
    for sc in scs:
        courses.append(sc.course)
    context = {
        'courses': courses,
        'stu': stu,
    }
    return render(request, 'student/courseLoved.html', context=context)


# 预选课按钮
def get_pre(request, s_id, c_id):
    co = Course.objects.get(c_id=c_id)
    try:
        Pre.objects.get(student=Student.objects.get(s_id=s_id), course=co)
    except:
        c = Pre(student=Student.objects.get(s_id=s_id), course=co)
        c.save()
        co.hot_value += 1
        co.save()
    return redirect(reverse('courseselect:select'))


# 取消预选课
def drop_pre(request, s_id, c_id):
    co = Course.objects.get(c_id=c_id)
    cs = Pre.objects.filter(student=Student.objects.get(s_id=s_id), course=co)
    for c in cs:
        c.delete()
    co.hot_value -= 1
    co.save()
    return redirect(reverse('courseselect:preselected'))


# 预选课界面选择按钮
def get_course_pre(request, s_id, c_id):
    now = timezone.now()
    date = Date.objects.all()[0]
    if now < date.start_time:
        return HttpResponse("选课尚未开始")
    if now > date.end_time:
        return HttpResponse("选课已经结束")
    full = is_full(c_id)
    courses = []
    aim_course = get_object_or_404(Course, c_id=c_id)
    scs = StudentCourse.objects.filter(student=Student.objects.get(s_id=s_id))
    for sc in scs:
        courses.append(sc.course)
    tag, conflict = allow(aim_course, courses)
    if tag and not full:
        c = StudentCourse(student=Student.objects.get(s_id=s_id), course=Course.objects.get(c_id=c_id))
        c.save()
        c1 = Pre.objects.get(student=Student.objects.get(s_id=s_id), course=Course.objects.get(c_id=c_id))
        c1.delete()
        aim_course.selected_now += 1
        aim_course.save()
        return redirect(reverse('courseselect:preselected'))
    elif not tag and not full:
        return HttpResponse("与" + conflict.name + '冲突')
    else:
        return HttpResponse("选课人数已满")


# 公告内容
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
    }
    post.body = markdown.markdown(
        post.body,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ]
    )
    return render(request, 'student/courseAnnuText.html', context=context)



# 教师模块------------------------------------------------以下已经改动-----------------------------

# 选课公告
def tea_courseAnnunciate(request):
    if not request.session.get('is_login', None):
        return redirect('courseselect:index')
    tea_id = request.session['id']
    context = {}
    list = []
    now = timezone.now()
    context['list'] = list
    teacher = Teacher.objects.get(t_id=tea_id)
    context['name'] = teacher.name
    time = Date.objects.all()[0]
    if now < time.start_time:
        is_start = 0
    else:
        is_start = 1
    context['is_start'] = is_start
    context['time'] = time


    return render(request, 'teacher/courseAnnunciate.html', context)


# 选课结果
def tea_courseResult(request):
    if not request.session.get('is_login', None):
        return redirect('courseselect:index')
    tea_id = request.session['id']
    courses = Course.objects.filter(teacher=Teacher.objects.get(t_id=tea_id))

    context = {}
    teacher = Teacher.objects.get(t_id=tea_id)
    context['name'] = teacher.name
    list = []
    for course in courses:
        list.append({"course_no": course.c_id, "subject_name": course.name, "department": course.department
                        , "credit": course.credit, "place": course.classroom, "start_week": course.start_week,
                     "end_week": course.end_week
                        , "course_section": str(course.start_time) + '-' + str(course.end_time), "course_weekday": course.weekdays,
                     "check_people": course.selected_now, "people_max": course.selected_limit})

    context['list'] = list

    return render(request, 'teacher/courseResult.html', context)


# 教师课表
def tea_mySchedule(request):
    if not request.session.get('is_login', None):
        return redirect('courseselect:index')
    tea_id = request.session['id']
    teacher = Teacher.objects.get(t_id=tea_id)
 
    scs = TeacherCourse.objects.filter(teacher=teacher)
    courses = []
    for sc in scs:
        courses.append(sc.course)
    context = {
        'name': teacher.name,
        'courses': courses,
    }
    courses = sorted(courses, key=lambda course: course.weekdays)

    return render(request, 'teacher/mySchedule.html', context)


# 选课成绩录入界面
def tea_courseScore(request):
    if not request.session.get('is_login', None):
        return redirect('courseselect:index')
    tea_id = request.session['id']
    courses = Course.objects.filter(teacher=Teacher.objects.get(t_id=tea_id))
    context = {}

    teacher = Teacher.objects.get(t_id=tea_id)
    context['name'] = teacher.name

    list = []
    for course in courses:
        scs = StudentCourse.objects.filter(course=course)
        students = []
        for sc in scs:
            student = {"stu_name": sc.student.name, "stu_no": sc.student.s_id, "stu_academy": sc.student.department,
                       "grade": sc.grade}
            students.append(student)
        list.append({"course_name": course.name, "course_no": course.c_id, "students": students})
    context['course_all'] = list
    return render(request, 'teacher/courseScore.html', context)


# 返回录入课程成绩模板
def tea_download_file(request):
    if not request.session.get('is_login', None):
        return redirect('courseselect:index')
    # 获取教师编号，课程编号
    course_no = api = request.GET.get("course_no")
    # 根据课程编号获取数据库中的学生选课数据
    scs = StudentCourse.objects.filter(course=Course.objects.get(c_id=course_no))

    curPath = os.path.abspath(os.path.dirname(__file__))
    filename = course_no + '_course.xls'
    file = "templates/" + filename
    filepath = os.path.join(curPath, file)

    # 因为输入都是Unicode字符，这里使用utf-8，免得来回转换
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

    booksheet.write(0, 0, "学号")
    booksheet.write(0, 1, "姓名")
    booksheet.write(0, 2, "成绩")
    i = 1
    for sc in scs:
        booksheet.write(i, 0, str(sc.student.s_id))
        booksheet.write(i, 1, str(sc.student.name))
        booksheet.write(i, 2, "")
        i = i + 1

        # 保存文件
    workbook.save(filepath)

    fp = open(filepath, 'rb')
    response = FileResponse(fp)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="' + filename + '"'
    print('attachment;filename=' + '"' + filename + '"')
    print(response['Content-Disposition'])
    return response
    fp.close()


# 根据教师上传的课程成绩表将成绩录入数据库
@csrf_exempt
def tea_uploadScore(request):
    if not request.session.get('is_login', None):
        return redirect('courseselect:index')
    course_no = request.POST.get('course_no')
    # 1 获取前端传输的文件对象,并将其写入内存
    try:
        file_obj = request.FILES.get('file')
    except:
        response = {}
        response['msg'] = "加载文件失败"
        return JsonResponse(response)
    file = "templates/" + file_obj.name
    curPath = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(curPath, file)
    try:
        fp = open(path, 'wb+')
    except:
        response = {}
        response['msg'] = "打开文件失败"
        return JsonResponse(response)
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
    for row in range(1, nrows):
        s_id = mySheet.cell_value(row, 0)
        grade = mySheet.cell_value(row, 2)
        st = StudentCourse.objects.get(student=Student.objects.get(s_id=s_id),
                                       course=Course.objects.get(c_id=course_no))
        st.grade = float(grade)
        st.save()

        # 给服务器返回信息
    response = {}
    response['msg'] = "操作成功"
    return JsonResponse(response)


# 获取课程对应的选课学生信息
def tea_getStuMsg(request):
    if not request.session.get('is_login', None):
        return redirect('courseselect:index')
        # 1 获取课程编号
    course_no = request.GET.get("course_no")
    # 2 根据课程编号获取对应课程的学生信息
    sts = StudentCourse.objects.filter(course=Course.objects.get(c_id=course_no))

    # 3 将学生信息写入文件
    curPath = os.path.abspath(os.path.dirname(__file__))
    filename = course_no + '_course_stuMsg.xls'
    file = "templates/" + filename
    filepath = os.path.join(curPath, file)

    # 因为输入都是Unicode字符，这里使用utf-8，免得来回转换
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

    booksheet.write(0, 0, "学号")
    booksheet.write(0, 1, "姓名")

    i = 1
    for st in sts:
        booksheet.write(i, 0, str(st.student.s_id))
        booksheet.write(i, 1, st.student.name)
        i = i + 1

        # 保存文件
    workbook.save(filepath)

    # 4将文件返回给请求源

    fp = open(filepath, 'rb')
    response = FileResponse(fp)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="' + filename + '"'
    return response
    fp.close() 