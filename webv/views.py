import rest_framework
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.response import Response

from api.views import *
from rest_framework_jwt.views import obtain_jwt_token


# Create your views here.

def show_r(request):
    response = (RecordList.as_view()(request))
    # print(response.render().readable())
    print(obtain_jwt_token(request))
    # Response().render().set_cookie('token', )
    # return response
    return obtain_jwt_token(request)
    # print(context)
    # return render(request, 'webv/index.html', context=context)
    # return context
