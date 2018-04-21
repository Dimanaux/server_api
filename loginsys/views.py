from django.shortcuts import render

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from webapp.views import my_profile


@csrf_exempt
def login(request):

    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username ,password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('my_profile', request)
        else:
            return render(request, "loginsys/login.html")
    else:
        return render(request, 'loginsys/login.html')


def logout(request):
    auth.logout(request)
    return redirect("/")

@csrf_exempt
def login_existence(request):
    if request.POST:
        username = request.POST.get('username', '')
        if User.objects.filter(username=username):
            return HttpResponse("error", content_type="text/plain")
        return HttpResponse("success", content_type="text/plain")

@csrf_exempt
def register(request):

    if request.POST:
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')



        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        # Автроризируемся!
        user = auth.authenticate(username=username, password=password1)
        if user is not None:
            auth.login(request, user)
            return redirect('/home.html')
        else:

            return render(request, "loginsys/register.html")
    else:
        return render(request, 'loginsys/register.html')