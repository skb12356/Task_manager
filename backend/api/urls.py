from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    CreateUserView,
    MemberCreateList,
    CookieLoginView,
    ProtectedMemberView,
    ProjectViewSet,
    ChatMessageViewSet,
    CompanyRegistrationView,
    LogoutView,
)

# Create and register viewsets with router
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'chat', ChatMessageViewSet, basename='chat')

urlpatterns = [
    path('members/', MemberCreateList.as_view(), name='members'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('cookie-login/', CookieLoginView.as_view(), name='cookie_login'),
    path('protected/', ProtectedMemberView.as_view(), name='protected'),
    path('register-company/', CompanyRegistrationView.as_view(), name='register-company'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Include router-generated URLs
    path('', include(router.urls)),
]
