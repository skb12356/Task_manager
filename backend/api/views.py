from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Member ,Project,ChatMessage
from .serializers import MemberSerializer,UserSerializer,ProjectSerializer,ChatMessageSerializer,CompanyRegistrationSerializer
from django.db import IntegrityError
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .authentication import CookieJWTAuthentication
from rest_framework import viewsets


class MemberCreateList(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Get all members with their related user data
        members = Member.objects.all().prefetch_related('user')
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'email': request.data.get('email')
        }
        
        # Create the User first
        try:
            user = User.objects.create_user(
                username=user_data['username'],
                password=user_data['password'],
                email=user_data['email']
            )
        except IntegrityError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Then create the Member profile
        member_data = {
            'mobile_no': request.data.get('mobile_no'),
            'dob': request.data.get('dob'),
            'address': request.data.get('address')
        }
        
        serializer = MemberSerializer(data=member_data)
        if serializer.is_valid():
            member = serializer.save(user=user)
            return Response(
                {
                    'message': 'Member created successfully',
                    'member_id': member.id,
                    'username': user.username
                },
                status=status.HTTP_201_CREATED
            )
        
        # If member creation fails, clean up the user
        user.delete()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateUserView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # backend/views.py (or wherever your views are)
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

@ensure_csrf_cookie  # Ensures the CSRF token is set in the cookie
def get_csrf_token(request):
    return JsonResponse({"status": "CSRF cookie set"})


class MemberTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Check if the user is a registered member
        if not Member.objects.filter(user=self.user).exists():
            raise serializers.ValidationError("You are not authorized to log in.")

        return data

class MemberTokenObtainPairView(TokenObtainPairView):
    serializer_class = MemberTokenObtainPairSerializer

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class CookieLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Only allow members to log in
        if not Member.objects.filter(user=user).exists():
            return Response({'error': 'Not authorized as a registered member'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=False,  # Set to True in production
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite='Lax'
        )

        return response

class ProtectedMemberView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": f"Welcome, {request.user.username}!"})
    

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

class CompanyRegistrationView(APIView):
    def post(self, request):
        serializer = CompanyRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Company registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({"detail": "Refresh token not provided"}, status=400)

        request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)

        # Set new access token in cookie
        if response.status_code == 200:
            access_token = response.data['access']
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                samesite='Lax',
                secure=False,
            )
            del response.data['access']

        return response
class LogoutView(APIView):
    def post(self, request):
        response = Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        # Delete the JWT cookies by setting empty values and expiry in the past
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

# class CookieProtectedView(APIView):
#     def get(self, request):
#         raw_token = request.COOKIES.get("access_token")
#         validated_token = JWTAuthentication().get_validated_token(raw_token)
#         user = JWTAuthentication().get_user(validated_token)
#         return Response({"message": f"Hello, {user.username}"})