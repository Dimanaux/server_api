# -*- coding: utf-8 -*-

"""tr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from api import views


urlpatterns = [
    url(r'users/', views.UserList.as_view(), name='user-list'),
    url(r'records/', views.RecordList.as_view(), name='records-list'),
    url(r'^api-token-auth/', obtain_jwt_token),
]
