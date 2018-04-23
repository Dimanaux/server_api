# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import generics, mixins, status

from api.models import Record, Profile, Game
from api.serializers import  RecordSerializer, ProfileSerializer, RegistrateSerializer, LoginSerializer, CreateRecordSerializer


class RegistrateUser(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = RegistrateSerializer
    permission_classes = [AllowAny]


class CreateRecord(CreateAPIView):
    # Todo:data validation in serializer
    serializer_class = CreateRecordSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        game = request.data['game']
        score = request.data['score']
        game = Game.objects.get(id=game)
        record = Record(user=user, game=game, score=score)
        record.save()

        return Response("succesfully created", status=status.HTTP_201_CREATED)


class MyRecordList(generics.ListAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        game = request.data['game']
        records = Record.objects.filter(user=user).filter(game_id=game)
        if len(request.data) == 1:
            quantity = 10
        else:
            quantity = request.data['quantity']
        real_quantity = records.count()
        if (real_quantity < quantity):
            quantity = real_quantity

        records = records.order_by('-score')[0:quantity]

        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)


class RecordList(generics.ListCreateAPIView):
    # Todo: add game.title and username instead of game&user

    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        game = request.data['game']
        records = Record.objects.filter(game__id=game)

        if len(request.data) == 1:
            quantity = 10
        else:
            quantity = request.data['quantity']
        real_quantity = records.count()
        if real_quantity < quantity:
            quantity = real_quantity

        records = records.order_by('-score')[0:quantity]
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)


class MyProfile(APIView):

    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = self.serializer_class({"pk": profile.pk, "username": profile.username, "company": profile.company,
                                            "company_name": profile.company.company_name,
                                            "is_company_manager": profile.is_company_manager})
        # serializer = self.serializer_class({"username":profile.username,
        # "company":profile.company.company_name,
        # "is_company_manager":profile.is_company_manager})

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
