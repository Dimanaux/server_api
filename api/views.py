# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, status

from api.models import Record, Profile, Game
from api.serializers import UserSerializer, RecordSerializer, ProfileSerializer, RegistrateSerializer, LoginSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication, BaseJSONWebTokenAuthentication


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAdminUser)


class RegistrateUser(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = RegistrateSerializer
    permission_classes = [AllowAny]


# class CreateRecord(APIView):
#     serializer_class = RecordSerializer
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#
#         # Todo: validation in serializer
#
#         data = request.data
#         user = self.request.user
#         game = Game.objects.get(data['game'])
#         score = data['score']
#         serializer = self.serializer_class(user=user,game=game,score=score)
#         if serializer.is_valid(raise_exception=True):
#             new_data = serializer.data
#             return Response(new_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyRecordList(generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        title = request.data['game']
        records = Record.objects.filter(user=user)
        records.filter(game__title=title)
        if len(request.data) == 1:
            quantity = 10
        else:
            quantity = request.data['quantity']
        real_quantity = records.count()
        if (real_quantity < quantity):
            count = real_quantity

        records = records.order_by('-score')[0:quantity]
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)


class RecordList(generics.ListCreateAPIView):
    # Todo: add game.title and username istead of game&user

    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        title = request.data['game']
        records = Record.objects.filter(game__title=title)

        if len(request.data) == 1:
            quantity = 10
        else:
            quantity = request.data['quantity']
        real_quantity = records.count()
        if real_quantity < quantity:
            count = real_quantity

        records = records.order_by('-score')[0:quantity]
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)


class MyProfile(APIView):
    # Todo: add company_name field instead of company

    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# idk what it is
def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()



#forms.py
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('url', 'location', 'company')

'''
