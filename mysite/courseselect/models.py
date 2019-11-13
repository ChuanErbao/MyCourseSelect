from django.db import models
import datetime
from django.utils import timezone


# Create your models here.


class User(models.Model):
    attribute = (
        ('teacher', '教师'),
        ('student', '学生'),
    )
    u_id = models.CharField(max_length=20, unique=True, primary_key=True, verbose_name='用户名')  # 用户名（学号/工号）
    password = models.CharField(max_length=20, default='123')           # 用户密码
    kind = models.CharField(max_length=10, choices=attribute, default='学生', verbose_name='用户属性')  # 用户属性 教师/学生
    c_time = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(verbose_name='电子邮件', default='wangjian192@mails.ucas.edu.cn')

    def __str__(self):
        return self.u_id

    class Meta:
        ordering = ['c_time']
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
    attribute = [
        ('compulsory', '必修课'),
        ('elective', '选修课')
    ]
    name = models.CharField(max_length=40, verbose_name='课程名称')
    kind = models.CharField(max_length=10, choices=attribute, verbose_name='课程类别', default='必修课')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属院系')
    pub_date = models.DateField(verbose_name='发布时间')
    credit = models.FloatField(verbose_name='学分')
    # 要有当前选课人数和选课人数上限
    selected_now = models.IntegerField(verbose_name='已选课人数', default=0)
    selected_limit = models.IntegerField(verbose_name='选课人数上限', )
    # students = models.ManyToManyField(Student, verbose_name='选课学生')
    # 上课时间，包括周次和节次，节次使用1-55表示
    start_week = models.IntegerField(verbose_name='开始周次', default=1)
    end_week = models.IntegerField(verbose_name='结束周次', default=20)
    arr_course = models.IntegerField(verbose_name='第几节', default=0)
    # 上课教室
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='上课教室')
    teacher = models.ManyToManyField(
        Teacher,
        verbose_name="授课教师",
    )
    # description = models.TextField(null=False)

    def set_pub_date(self):
        self.pub_date = datetime.time

    class Meta:
        ordering = ['pub_date', 'department']
        verbose_name_plural = '课程'

    def __str__(self):
        return self.name


class Student(models.Model):
    s_id = models.ForeignKey(User, verbose_name='学号', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='姓名')
    courses = models.ManyToManyField(Course, verbose_name='已选课程')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属院系')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '学生'


# 突然意识到这个就可以做成绩表
class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField(verbose_name='成绩', default='0')

    def __str__(self):
        return self.student.name + '的课程及成绩'


class TeacherCourse(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='授课教师')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')

    def __str__(self):
        return self.teacher + '所教授的' + self.course


# # 应该怎么实现课程冲突判断
# class ClassroomTime(models.Model):
#     classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='教室')
#     week =

