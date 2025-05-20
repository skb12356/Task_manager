from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Member
from .models import Project, ChatMessage
from .models import Company

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



class ChatMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'project', 'sender', 'sender_username', 'message', 'timestamp']

class ProjectSerializer(serializers.ModelSerializer):
    chat = ChatMessageSerializer(many=True, read_only=True)  # reverse related_name='chat'

    class Meta:
        model = Project
        fields = ['id', 'name', 'status', 'members', 'warehouse', 'chat', 'company_id']


class CompanyRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    company_name = serializers.CharField(write_only=True)
    company_id = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ['username', 'password', 'company_name', 'company_id']

    def validate_company_id(self, value):
        if Company.objects.filter(company_id=value).exists():
            raise serializers.ValidationError("Company ID already exists.")
        return value

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        company_name = validated_data.pop('company_name')
        company_id = validated_data.pop('company_id')

        user = User.objects.create_user(username=username, password=password)
        company = Company.objects.create(owner=user, name=company_name, company_id=company_id)
        return company