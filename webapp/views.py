import sqlite3

from django.contrib.auth.decorators import login_required
# from django.contrib.messages import api
from django.shortcuts import render

import api

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from api.models import Profile, Company, DEFAULT_COMPANY_NAME


@login_required(redirect_field_name='login')
def my_profile(request):
    user = auth.get_user(request)

    profile = Profile.objects.get(user=user)
    context = {'company': profile.company.company_name, 'username': profile.username}

    return render(request, 'webapp/my_profile.html', context)


@csrf_exempt
def login(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('my_profile')
        else:
            return render(request, "webapp/login.html", {'error': 'неверный логин или пароль'})
    else:
        return render(request, 'webapp/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


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
        company_name = request.POST.get('company_name', DEFAULT_COMPANY_NAME)
        if company_name == '':
            company_name = DEFAULT_COMPANY_NAME

        if Company.objects.filter(company_name=company_name).exists():
            company = Company.objects.get(company_name=company_name)
        else:
            company = Company(company_name=company_name)
            company.save()

        user = User.objects.create_user(username=username, email=email, password=password1)
        profile = Profile(user=user, company=company, is_company_manager=is_company_manager)

        try:
            user.save()
            profile.save()
        except sqlite3.IntegrityError:
            return HttpResponse("This username is already reserved.")

        user = auth.authenticate(username=username, password=password1)
        if user is not None:
            auth.login(request, user)
            return redirect('my_profile')
        else:
            return render(request, "webapp/registration.html")
    else:
        return render(request, 'webapp/registration.html')
