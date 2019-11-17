from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from courseselect.models import User, Student, Teacher
from email.mime.text import MIMEText
import smtplib
import json
import random
from .forms import UserForm


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            u_id = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            kind = form.cleaned_data['kind']
            request.session['id'] = u_id
            try:
                user = User.objects.get(pk=u_id)
            except:
                return HttpResponse('用户不存在！')
            if user.kind != kind:
                return HttpResponse('请选择正确的用户类型！')
            else:
                if user.password != pwd:
                    return HttpResponse('用户名或密码错误！')
                else:
                    request.session['is_login'] = True
                    if kind == 'student':
                        stu = get_object_or_404(Student, s_id=u_id)
                        context = {'name': stu.name}
                        return render(request, 'student/courseAnnunciate.html', context=context)
                    else:
                        tea = get_object_or_404(Teacher, t_id=u_id)
                        context = {'name': tea.name}
                        return render(request, 'teacher/courseAnnunciate.html', context=context)
    else:
        form = UserForm()
    return render(request, 'index.html', context={'form': form})


def forget_password(request): 
    return render(request,'forgetPsw.html') 

# def login_check(request):
#     response={}
#     # 获取传入数据
#     try:
#         username=request.GET.get("user")
#         password=request.GET.get("password")
#         typeId=request.GET.get("typeId")
#         print(typeId,"--------------------------------")
#     except:
#         return HttpResponse("参数错误！")
#
#     # 获取数据库数据
#     try:
#         user=User.objects.get(username=username)
#         if user.password==password and str(user.role)==typeId:
#             response["res"]="2"
#             if user.role==1:
#                 response["url"]="/course_select/forget_password/"
#             elif user.role==2:
#                 response["url"]="/select_course/teacher/courseAnnunciate"
#             data=[{"stu_name","wanghualei"}]
#             response["data"]=str(data)
#         else:
#             response["res"]="0"
#             response["msg"]="密码错误"
#     except:
#         response["res"]="0"
#         response["msg"]="账号不存在"
#     # 返回JSON数据
#     # 需要跳转的路径，这里写成忘记密码界面
#     # return HttpResponse(json.dumps(response),content_type='application/json')
#     # Django 1.7版本之后的快捷操作
#     return JsonResponse(response)


verification =""

def forget_password_do(request):
    global verification
    response={}
    api=request.GET.get("api") 
    print(api)
    if api=="findInformation":
        try:
            username=request.GET.get("user")
            api=request.GET.get("api")
            typeId=request.GET.get("typeId")
        except:
            response["res"]="0"
            return JsonResponse(response)

        # 获取数据库数据
        try:
            user=User.objects.get(username=username) 
            if str(user.role)==typeId: 
                print(typeId)
                response["res"]="2"
                response["mail_address"]=user.mail_address 
            else: 
                response["res"]="0"
        except: 
            response["res"]="0" 
        return JsonResponse(response)
    elif api=="sendVerification":
        mail_address=request.GET.get("mail_address")
        time=request.GET.get("time") 

        verification = ""
        # 生成验证码
        for i in range(6):    
            num = random.randrange(0, 4)    
            if num == 3 or num == 1:        
                rad2 = random.randrange(0, 10)       
                verification = verification + str(rad2)    
            else:        
                rad = random.randrange(65, 91)        
                c = chr(rad)        
                verification = verification + c  
        msg = MIMEText(verification)
        # 设置邮件主题
        msg["Subject"] = "国科大选课密码重置" 
        # 寄件者
        msg["From"]= '国科大'
        # 收件者
        msg["To"]= '学生'

        from_addr = "2243829852@qq.com"
        password = "gypadmissdsnebjb"
        # smtp服务器地址
        smtp_server = 'smtp.qq.com'
        # 收件人地址
        to_addr = mail_address

        try:
            # smtp协议的默认端口是25，QQ邮箱smtp服务器端口是465,第一个参数是smtp服务器地址，第二个参数是端口，第三个参数是超时设置,这里必须使用ssl证书，要不链接不上服务器
            server = smtplib.SMTP_SSL(smtp_server, 465, timeout = 2)
            # 登录邮箱
            server.login(from_addr, password)
            #发送邮件，第一个参数是发送方地址，第二个参数是接收方列表，列表中可以有多个接收方地址，表示发送给多个邮箱，msg.as_string()将MIMEText对象转化成文本
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()
            response["res"]="2" 
        except:
            response["res"]="0" 
        return JsonResponse(response)
    elif api=="findPassword": 
        username=request.GET.get("user")
        typeId=request.GET.get("typeId")
        send_verification=request.GET.get("verification")  
        mail_address=request.GET.get("mail_address") 
        password=request.GET.get("password")
        print("....................................1")
        print(send_verification)
        print(verification)
        # 为了方便测试，111111为默认可通过的验证码
        if send_verification==verification or send_verification=="111111": 
            user=User.objects.get(username=username)
            user.password=password
            user.save() 
            response["res"]="2"
        else:
            response["res"]="0"
            response["msg"]="验证码错误！" 
        return JsonResponse(response)