from django.db import transaction
from django.http import HttpRequest, HttpResponse
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework import status

from apps.wallets.models import Wallet
from .serialiers import (
    UserRegistrationRequestSerializer,
    UserRefreshRequestSerializer
)
from .models import User
from .services import (
    get_token_http_reponse,
    get_logout_http_response
)


@extend_schema(
    summary="Sign-up by email and password",
    description="Take email and password, create user and default wallet",
    request=UserRegistrationRequestSerializer,
    methods=["POST"],
    responses={
        201: OpenApiResponse(description="Successfully registrated."),
        400: OpenApiResponse(description="Error: Bad request"),
        404: OpenApiResponse(description="Error: Not found"),
        422: OpenApiResponse(description="Error: Unprocessable entity"),
        500: OpenApiResponse(description="Error: Internal server error"),
    },
    tags=[
        "auth",
    ],
)
@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def sign_up(request: HttpRequest) -> HttpResponse:

    data = JSONParser().parse(request)
    serializer = UserRegistrationRequestSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    created_user = User.objects.create_user(
        email=serializer.validated_data["email"],
        password=serializer.validated_data["password"]
    )
    Wallet.objects.create(user=created_user)

    return HttpResponse(status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Sign-in by email and password",
    description="Take user's email and password and return 'access' and 'refresh' tokens in cookies",
    request=UserRegistrationRequestSerializer,
    methods=["POST"],
    responses={
        200: OpenApiResponse(description="Successfully signed-in."),
        500: OpenApiResponse(description="Error: Internal server error"),
    },
    tags=[
        "auth",
    ],
)
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in(request: HttpRequest) -> HttpResponse:
    data = JSONParser().parse(request)
    email = data["email"]
    password = data["password"]

    try:
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise AuthenticationFailed()
    except User.DoesNotExist:
        raise AuthenticationFailed()

    return get_token_http_reponse(user)


@extend_schema(
    summary="Sign-in by email and password",
    description="Take user's email and password and return 'access' and 'refresh' tokens in cookies",
    request=UserRegistrationRequestSerializer,
    methods=["POST"],
    responses={
        200: OpenApiResponse(description="Successfully signed-in."),
        500: OpenApiResponse(description="Error: Internal server error"),
    },
    tags=[
        "auth",
    ],
)
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in(request: HttpRequest) -> HttpResponse:
    data = JSONParser().parse(request)
    email = data["email"]
    password = data["password"]

    try:
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise AuthenticationFailed()
    except User.DoesNotExist:
        raise AuthenticationFailed()

    return get_token_http_reponse(user)


@extend_schema(
    summary="Logout",
    description="Take authenticated user's refresh token, revoke it and blacklist it",
    methods=["POST"],
    request=None,
    responses={
        204: OpenApiResponse(description="Successfully logged out."),
        400: OpenApiResponse(description="Error: Refresh token is required."),
        401: OpenApiResponse(description="Error: Authentication credentials were not provided."),
        422: OpenApiResponse(description="Error: Token is invalid or expired"),
    },
    tags=[
        "auth",
    ],
)
@api_view(["POST"])
def logout(request: HttpRequest) -> HttpResponse:

    data = {"refresh": request.COOKIES.get("refresh")}
    serialized_token = UserRefreshRequestSerializer(data=data)
    serialized_token.is_valid(raise_exception=True)

    return get_logout_http_response(token=serialized_token.data.get("refresh"))
