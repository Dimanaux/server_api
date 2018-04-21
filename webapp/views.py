import sqlite3

from django.shortcuts import render

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from api.models import Profile, Company


def my_profile():
    pass


@csrf_exempt
def login(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('my_profile', request)
        else:
            return render(request, "loginsys/login.html")
    else:
        return render(request, 'loginsys/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login', request)


# @csrf_exempt
# def login_existence(request):
#     if request.POST:
#         username = request.POST.get('username', '')
#         if User.objects.filter(username=username):
#             return HttpResponse("error", content_type="text/plain")
#         return HttpResponse("success", content_type="text/plain")


@csrf_exempt
def register(request):
    if request.POST:
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        is_company_manager = request.POST.get('is_company_manager', False)
        company_name = request.POST.get('company_name', 'Train Rabbits')

        company = Company.objects.get(company_name=company_name)
        user = User(username=username, email=email, password=password1)
        profile = Profile(user=user, company=company, is_company_manager=is_company_manager)

        try:
            user.save()
            profile.save()
        except sqlite3.IntegrityError:
            return HttpResponse("This username is already reserved.")

        user = auth.authenticate(username=username, password=password1)
        if user is not None:
            auth.login(request, user)
            return redirect('register')
        else:
            return render(request, "webapp/registration.html")
    else:
        return render(request, 'webapp/registration.html')
