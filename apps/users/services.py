from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken


def get_token_http_reponse(user, refresh_token: str = None) -> HttpResponse:
    http_response = HttpResponse(status=200)
    if refresh_token:
        token = RefreshToken(token=refresh_token)
    else:
        token = RefreshToken.for_user(user)
        http_response.set_cookie("refresh", str(token), httponly=True)
    http_response.set_cookie("access", str(token.access_token), httponly=True)
    return http_response


def get_logout_http_response(token: str) -> HttpResponse:
    token = RefreshToken(token)
    token.blacklist()
    http_response = HttpResponse(status=204)
    http_response.delete_cookie("access")
    http_response.delete_cookie("refresh")
    return http_response
