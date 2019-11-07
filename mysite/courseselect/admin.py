from django.contrib import admin
from .models import *

# Register your models here.
# admin 123

# 自定义管理员界面标题
admin.site.site_header = '中国科学院大学选课系统后台管理'
admin.site.site_title = '后台管理'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ('c_id', 'name', 'teacher', 'department', 'pub_date',)
    list_display = ['c_id', 'name', '授课教师', 'department', 'pub_date']
    # list_display_links = ['name']
    list_filter = ['department']
    search_fields = ['name', ]
    filter_horizontal = ('teacher',)  # 只针对多对多

    # actions_on_top = True
    # actions_on_bottom = True
    # save_on_top = True

    def 授课教师(self, obj):
        return [t.name for t in obj.teacher.all()]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fields = ('t_id', 'name', 'department')
    list_display = ['t_id', 'name', 'department']
    list_filter = ['department']
    search_fields = ['name', ]

    # 可以写一个课程数量统计


@admin.register(Student)
class Student(admin.ModelAdmin):
    fields = ('s_id', 'name', 'department')
    list_display = ['s_id', 'name', 'department']
    list_filter = ['department']
    search_fields = ['name', ]

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    fields = ('d_id', 'name')
    list_display = ['d_id', 'name']
    search_fields = ['name', ]
