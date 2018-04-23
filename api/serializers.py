from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CharField

from api.models import (Game, Record, Profile, Company)
from rest_framework.serializers import (EmailField, ValidationError)
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    company_name = serializers.CharField(allow_blank=True)

    class Meta:
        model = Profile
        fields = ('pk', 'username', 'company', 'company_name', 'is_company_manager')

        # fields = ('username', 'company','is_company_manager')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True, allow_blank=True)

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']

        if username is None:
            raise serializers.ValidationError(
                'An username address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        attrs['token'] = token

        return attrs


class RegistrateSerializer(serializers.ModelSerializer):
    username = CharField()
    password1 = CharField(write_only=True)
    password2 = CharField(write_only=True)
    company_name = CharField()
    email = EmailField(label="Email Address")
    token = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('username', 'company_name', 'is_company_manager', 'password1', 'password2', 'email', 'token')

        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password1 = attrs['password1']
        password2 = attrs['password2']
        username = attrs['username']
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            raise ValidationError("this username is already used")
        if password1 != password2:
            raise ValidationError("passwords must match")
        return attrs

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        company_name = validated_data['company_name']
        password1 = validated_data['password1']
        is_company_manager = validated_data['is_company_manager']
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        if Company.objects.filter(company_name=company_name).exists():
            company = Company.objects.get(company_name=company_name)
        else:
            company = Company(company_name)
            company.save()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        validated_data['token'] = token

        profile = Profile(user=user, company=company, is_company_manager=is_company_manager)
        profile.save()
        return validated_data


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = (
            'user',
            'game',
            'score',
            # 'date',
        )


class CreateRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('game', 'user', 'score')

