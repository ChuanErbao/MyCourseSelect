from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import User
import json

# Create your views here.
def login(request): 
    return render(request,'login.html')

def forgetpassword(request): 
    return render(request,'forgetPsw.html') 

def login_check(request): 

    response={}
    # 获取传入数据
    try:
        username=request.GET.get("user")
        password=request.GET.get("password")
        typeId=request.GET.get("typeId")
    except:
        return HttpResponse("参数错误！") 

    # 获取数据库数据
    try:
        user=User.objects.get(username=username) 
        if user.password==password:
            response["res"]="2"
            response["url"]="/course_select/forget_password/"
            data=[{"stu_name","wanghualei"}]
            response["data"]=str(data)
        else:
            response["res"]="0"
            response["msg"]="密码错误"
    except:
        response["res"]="0"
        response["msg"]="账号不存在" 
    # 返回JSON数据
    # 需要跳转的路径，这里写成忘记密码界面
    # return HttpResponse(json.dumps(response),content_type='application/json')
    # Django 1.7版本之后的快捷操作
    return JsonResponse(response)