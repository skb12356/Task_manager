# members/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
            user = self.get_user(validated_token)
        except InvalidToken:
            raise AuthenticationFailed("Invalid or expired token")

        return (user, validated_token)
# class CookieJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         access_token = request.COOKIES.get('access_token')

#         if access_token is None:
#             return None  # No token, let unauthenticated

#         try:
#             validated_token = self.get_validated_token(access_token)
#             user = self.get_user(validated_token)
#             return (user, validated_token)
#         except Exception as e:
#             raise AuthenticationFailed(f"Invalid token: {str(e)}")
