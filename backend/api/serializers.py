from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Member

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {'password': {'write_only': True}}

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Member
        fields = ['id', 'user', 'mobile_no', 'dob', 'address']
