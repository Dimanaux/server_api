from django.conf.urls import url, include
from django.contrib import admin
from .views import login,logout

urlpatterns = [
    url(r'^login/', login),
    url(r'^logout/', logout),
]