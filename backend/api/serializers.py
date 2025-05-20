from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Member
from .models import Project, ChatMessage

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
