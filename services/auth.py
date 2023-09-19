from django.conf import settings
from drf_spectacular.authentication import OpenApiAuthenticationExtension
from rest_framework.permissions import IsAuthenticated as _IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


class IsAuthenticated(_IsAuthenticated):
    def has_permission(self, request, view) -> bool:
        return request.auth is not None


class CookiesAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get(settings.REST_FRAMEWORK["JWT_AUTH_COOKIE"])
        return self.get_user_token_pair(token)

    def get_user_token_pair(self, token):
        try:
            validated_token = self.get_validated_token(token)
            user = self.get_user(validated_token)
            return user, validated_token
        except (InvalidToken, AuthenticationFailed):
            return None, None


class CookiesAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = CookiesAuthentication
    name = "Authorization"

    def get_authenticator(self):
        return self.target_class()

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "cookies",
            "name": "Authorization",
            "description": "Cookie-based authentication by 'access' token",
        }
