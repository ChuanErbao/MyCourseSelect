from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Course

# Create your views here.


def index(request):
    return HttpResponse("yingyingying")


def courses(request):
    cu = Course.objects.all()
    context = {'cus': cu}
    return render(request, 'courseselect/courses.html', context=context)
    # return HttpResponse("Teacher Page")