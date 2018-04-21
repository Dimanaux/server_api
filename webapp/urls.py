from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^my_profile', my_profile),
    url(r'^logout', logout),
    url(r'^login', login),
    url(r'^registration', register),
]

