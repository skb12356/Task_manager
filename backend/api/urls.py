from django.urls import path
from . import views
from .views import CreateUserView, MemberCreateList, CookieLoginView,ProtectedMemberView


urlpatterns = [
    path('members/', MemberCreateList.as_view(), name='members'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('cookie-login/', CookieLoginView.as_view(), name='cookie_login'),
     path('protected/', ProtectedMemberView.as_view(), name='protected'),

]
