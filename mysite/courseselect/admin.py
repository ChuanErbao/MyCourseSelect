from django.contrib import admin
from .models import User

# Register your models here.
# admin 123


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass