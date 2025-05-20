from django.contrib import admin
from django.urls import path, include
from api.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import get_csrf_token
from api.views import MemberTokenObtainPairView,CookieTokenRefreshView
  
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/token/', MemberTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
    path('api/csrf_token/', get_csrf_token, name='csrf_token'),
]
