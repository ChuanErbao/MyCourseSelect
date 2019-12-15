from django.db import models
import datetime
from django.utils import timezone
import markdown
from django.utils.html import strip_tags
from django.shortcuts import reverse
from tinymce.models import HTMLField


# Create your models here.


class User(models.Model):
    attribute = (
        ('teacher', '教师'),
        ('student', '学生'),
    )
    u_id = models.CharField(max_length=20, unique=True, primary_key=True, verbose_name='用户名')  # 用户名（学号/工号）
    password = models.CharField(max_length=20, default='123')           # 用户密码
    kind = models.CharField(max_length=10, choices=attribute, default='teacher', verbose_name='用户属性')  # 用户属性 教师/学生
    # c_time = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(verbose_name='电子邮件', default='wangjian192@mails.ucas.edu.cn')

    def __str__(self):
        return self.u_id

    class Meta:
        # ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Department(models.Model):
    d_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, verbose_name='院系名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '院系'


class Classroom(models.Model):
    attribute = [
        ('1', '教1'),
        ('2', '教2'),
    ]
    cm_id = models.AutoField(primary_key=True, verbose_name='教室编号')
    site = models.CharField(max_length=20, choices=attribute, default='教1')

    def __str__(self):
        return self.site

    class Meta:
        verbose_name_plural = '教室'


class Teacher(models.Model):
    t_id = models.ForeignKey(User, verbose_name='工号', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='姓名')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属院系')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '教师'


class Course(models.Model):
    c_id = models.AutoField(primary_key=True, verbose_name='课程id')
    # attribute = [
    #     ('学位课', '学位课'),
    #     ('非学位课', '非学位课')
    # ]
    name = models.CharField(max_length=40, verbose_name='课程名称')
    # kind = models.CharField(max_length=10, choices=attribute, verbose_name='课程类别', default='学位课')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属院系')
    pub_date = models.DateField(verbose_name='发布时间', default=timezone.now)
    credit = models.FloatField(verbose_name='学分')
    # 要有当前选课人数和选课人数上限
    selected_now = models.IntegerField(verbose_name='已选课人数', default=0)
    selected_limit = models.IntegerField(verbose_name='选课人数上限', )
    # students = models.ManyToManyField(Student, verbose_name='选课学生')
    # 上课时间，包括周次和节次，节次使用1-55表示
    start_week = models.IntegerField(verbose_name='开始周次', default=1)
    end_week = models.IntegerField(verbose_name='结束周次', default=20)
    weekdays = models.IntegerField(verbose_name='周几', default=0)
    start_time = models.IntegerField(verbose_name='开始节', default=0)
    end_time = models.IntegerField(verbose_name='结束节', default=0)
    hot_value = models.IntegerField(verbose_name='热度值', default=0)
    # 上课教室
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='上课教室')
    teacher = models.ManyToManyField(
        Teacher,
        verbose_name="授课教师",
    )
    # description = models.TextField(null=False)

    def set_pub_date(self):
        self.pub_date = datetime.time

    def teacherlist(self):
        return [t.name for t in self.teacher.all()]

    def get_weekday(self):
        return self.arr_course // 11 + 1;

    # def get_num(self):
    #     return self.arr_course % 11;

    def reset_hot_value(self):
        self.hot_value = 0

    class Meta:
        ordering = ['pub_date', 'department']
        verbose_name_plural = '课程'

    def __str__(self):
        return self.name


class Student(models.Model):
    s_id = models.OneToOneField(User, verbose_name='学号', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='姓名')
    courses = models.ManyToManyField(Course, verbose_name='已选课程')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属院系')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '学生'


# 突然意识到这个就可以做成绩表
class StudentCourse(models.Model):
    choice = [
        ('is', 'is'),
        ('not', 'not'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField(verbose_name='成绩', default='0')
    attribute = models.CharField(verbose_name='学位课',max_length=10,  choices=choice, default='not')

    def __str__(self):
        return self.student.name + '的课程及成绩'

    class Meta:
        verbose_name_plural = '选课及成绩'


# 预选课及热度排名
class Pre(models.Model):
    choice = [
        ('is', 'is'),
        ('not', 'not'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_loved = models.CharField(verbose_name='是否收藏', choices=choice,max_length=10, default='not')

    class Meta:
        verbose_name = '预选课'
        verbose_name_plural = '预选课'


class TeacherCourse(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='授课教师')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')

    def __str__(self):
        return self.teacher.name + '所教授的' + self.course.name


class Date(models.Model):
    start_time = models.DateTimeField(verbose_name='选课开始时间', default=timezone.now)
    end_time = models.DateTimeField(verbose_name='选课结束时间', default=timezone.now)

    class Meta:
        verbose_name_plural = '选课开始结束时间'
        verbose_name = '选课开始结束时间'


# # 应该怎么实现课程冲突判断
# class ClassroomTime(models.Model):
#     classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='教室')
#     week =

class Post(models.Model):
    title = models.CharField(max_length=20, verbose_name="公告标题")
    # body = models.TextField(verbose_name="正文")
    body = HTMLField(verbose_name="正文")
    created_time = models.DateTimeField(auto_now=True)
    excerpt = models.CharField(max_length=100, verbose_name="摘要")

    # # 复写save实现摘要功能
    # def save(self, *args, **kwargs):
    #     if not self.excerpt:
    #         md = markdown.Markdown(extensions=[
    #             'markdown.extensions.extra',
    #             'markdown.extensions.codehilite',
    #         ])
    #         self.excerpt = strip_tags(md.convert(self.body))[:54]
    #
    #     super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courseselect:post_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']
        verbose_name_plural = '公告'
        verbose_name = '公告'

