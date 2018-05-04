from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^my_profile', my_profile, name='my_profile'),
    url(r'^logout', logout, name='logout'),
    url(r'^login', login, name='login'),
    url(r'^registration', register, name='register'),
    url(r'',my_profile),
    url(r'^my_records',my_records,name='my_records'),
    url(r'^new_record', new_record, name='new_record'),
    
]

