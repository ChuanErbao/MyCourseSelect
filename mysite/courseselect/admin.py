from django.contrib import admin
from .models import *

# Register your models here.
# admin 123

# 自定义管理员界面标题
admin.site.site_header = '中国科学院大学选课系统后台管理'
admin.site.site_title = '后台管理'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('u_id', 'kind')
    list_display = ('u_id', 'kind')
    search_fields = ['u_id']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ('name', 'teacher', 'credit', 'department', 'start_week', 'end_week', 'arr_course', 'selected_limit', 'pub_date', 'classroom')
    list_display = ['c_id', 'name', '授课教师', 'department', '上课时间', 'credit', 'selected_now', 'selected_limit' ]
    # list_display_links = ['name']
    list_filter = ['department', 'credit']
    search_fields = ['name', 'teacher']
    filter_horizontal = ('teacher',)  # 只针对多对多

    # actions_on_top = True
    # actions_on_bottom = True
    # save_on_top = True

    def 授课教师(self, obj):
        return [t.name for t in obj.teacher.all()]

    def 上课时间(self, obj):
        return '第' + str(obj.start_week) + '周--第' + str(obj.end_week) + '周周' + str(obj.arr_course // 11 + 1) + '第' + str(obj.arr_course % 11 ) + '节'


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
    fields = ('name', )
    list_display = ['d_id', 'name']
    search_fields = ['name', ]


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    fields = ('site', )
    list_display = ['cm_id', 'site']
