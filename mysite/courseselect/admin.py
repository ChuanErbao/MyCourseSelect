from django.contrib import admin
from .models import Course

# Register your models here.
# admin 123


@admin.register(Course)
class UserAdmin(admin.ModelAdmin):
    pass