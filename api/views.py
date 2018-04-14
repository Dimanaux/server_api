from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser

from api.models import Record
from api.serializers import UserSerializer,RecordSerializer
from rest_framework import generics

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAdminUser)


class RecordList(generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


