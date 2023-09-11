from django.conf import settings
from rest_framework import exceptions, views
from rest_framework.exceptions import PermissionDenied

from .auth import CookiesAuthentication


def custom_exceptions_handler(exc, context):
    response = views.exception_handler(exc, context)
    token = context["request"].COOKIES.get(settings.REST_FRAMEWORK["JWT_AUTH_COOKIE"])
    user, _ = CookiesAuthentication().get_user_token_pair(token=token)
    if user is None:
        # manage the case of default DRF 403 PermissionDenied
        if isinstance(exc, PermissionDenied):
            exc = exceptions.NotAuthenticated()
            if token is not None:
                exc = exceptions.AuthenticationFailed()
            response.status_code = exc.status_code
            response.data["detail"] = exc.detail

    return response
