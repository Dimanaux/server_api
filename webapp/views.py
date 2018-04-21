from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from api.models import Profile,Record
from django.contrib.auth.models import User
from django.contrib import auth

@login_required
def my_profile(request):
    user = auth.get_user(request)
    # profile = Profile.objects.filter(user=user).get()
    # context = {'company':profile.company, 'username': profile.username}
    context = {'username':user.username}
    return render(request, 'loginsys/home.html', context)




