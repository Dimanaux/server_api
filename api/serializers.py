from django.contrib.auth.models import User,Group
from rest_framework import serializers
from api.models import Game,Record

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','user_name')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name')


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('user','game','score')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('title')