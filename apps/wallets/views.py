from django.http import HttpRequest, HttpResponse
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.models import User

from .models import Wallet
from .serialiers import WalletInfoSerializer


@extend_schema(
    summary="Get user's wallet balance",
    description="Take email and password, create user and set cookies",
    request=None,
    methods=["GET"],
    responses={
        200: OpenApiResponse(response=WalletInfoSerializer),
        400: OpenApiResponse(description="Error: Bad request"),
        404: OpenApiResponse(description="Error: Not found"),
        500: OpenApiResponse(description="Error: Internal server error"),
    },
    tags=[
        "wallet",
    ],
)
@api_view(["GET"])
def get_wallet_balance(request: HttpRequest) -> HttpResponse:
    wallet = Wallet.objects.get(user=request.user)

    return Response(
        data=WalletInfoSerializer(wallet).data, status=status.HTTP_201_CREATED
    )
