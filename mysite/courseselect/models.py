from django.db import models
import datetime

# Create your models here.


class Department(models.Model):
    d_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '院系'


# 为啥只有在Course前边才行
class Teacher(models.Model):
    t_id = models.AutoField(max_length=20, primary_key=True, verbose_name='工号')
    name = models.CharField(max_length=20, verbose_name='姓名')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属院系')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '教师'


class Course(models.Model):
    c_id = models.AutoField(primary_key=True, verbose_name='课程id')
    name = models.CharField(max_length=40, verbose_name='课程名称')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属院系')
    pub_date = models.DateField(verbose_name='发布时间')
    teacher = models.ManyToManyField(
        Teacher,
        verbose_name="授课教师",
    )
    description = models.TextField(null=False)

    def set_pub_date(self):
        self.pub_date = datetime.time

    class Meta:
        ordering = ['pub_date', 'department']
        verbose_name_plural = '课程'

    def __str__(self):
        return self.name


class Student(models.Model):
    s_id = models.CharField(max_length=20, primary_key=True, verbose_name='学号')
    name = models.CharField(max_length=20, verbose_name='姓名')
    courses = models.ManyToManyField(Course, verbose_name='已选课程', null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='所属院系')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '学生'


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)







