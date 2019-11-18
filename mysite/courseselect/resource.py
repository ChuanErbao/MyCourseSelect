from import_export import resources
from .models import *


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        import_id_fields = ('u_id', )
        fields = ('u_id', 'kind', 'email')
        export_fields = ('u_id', 'kind', 'email')


class StudentResource(resources.ModelResource):

    class Meta:
        model = Student
        import_id_fields = ('s_id', )
        fields = ('s_id', 'name', 'department', )
        export_fields = ('s_id', 'name', 'department',)


class TeacherResource(resources.ModelResource):

    class Meta:
        model = Teacher
        import_id_fields = ('t_id', 'department', 'credit', 'selected_limit', 'start_week', 'end_week', 'arr_course', 'classroom', 'teacher')
        fields = ('t_id', 'name', 'department', )
        export_fields = ('s_id', 'name', 'department',)


class CourseResource(resources.ModelResource):

    class Meta:
        model = Course
        fields = ('name', '')