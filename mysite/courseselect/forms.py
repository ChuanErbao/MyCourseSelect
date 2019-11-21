from django.forms import ModelForm
from .models import Course

from django import forms


class UserForm(forms.Form):
    choice = [
        ('teacher', '教师'),
        ('student', '学生'),
    ]
    username = forms.CharField(label='用户名：',max_length=100)
    password = forms.CharField(label='密码：',widget=forms.PasswordInput())
    kind = forms.ChoiceField(label='用户类型', choices=choice)


class SearchForm(forms.Form):
    content = forms.CharField(label='',max_length=20, initial='如：计算机')