from django.db import transaction
from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.pagination import LimitOffsetPagination
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from drf_spectacular.types import OpenApiTypes
from extentions import exceptions, TransactionTypesEnum

from ..models import UserCategory, Transaction
from ..serialiers import (
    TransactionSerializer,
    TransactionInfoSerializer,
    TransactionUpdateCategorySerializer,
)


@extend_schema(
    summary="Create transection",
    description="Create user's transaction",
    methods=["POST"],
    request=TransactionSerializer,
    parameters=[
        OpenApiParameter(
            name="category_id",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name='type',
            type=OpenApiTypes.STR,
            enum=[
                TransactionTypesEnum.income.value,
                TransactionTypesEnum.outcome.value,
            ],
            description='Type of transaction',
            required=True,
        ),
    ],
    responses={
        201: OpenApiResponse(response=TransactionSerializer),
        400: OpenApiResponse(description="Error: You do not have category with related ID."),
        401: OpenApiResponse(description="Error: Authentication credentials were not provided."),
        500: OpenApiResponse(description="Error: Internal server error."),
    },
    tags=[
        "transactions",
    ],
)
@api_view(['POST'])
@transaction.atomic
def create_transaction(request: HttpRequest):
    user_id = request.user.id
    category_id = request.GET.dict().get('category_id', None)
    data = JSONParser().parse(request)
    if category_id:
        if not UserCategory.objects.filter(id=category_id, user__id=user_id).exists():
            raise exceptions.BadRequest(detail='You do not have category with provided ID.')

    serializer = TransactionSerializer(
        data=data,
        context={
            'user_id': user_id,
            'category_id': category_id,
            'type': request.GET.get('type'),
        }
    )
    serializer.is_valid(raise_exception=True)
    created_transaction = serializer.save()
    return Response(data=TransactionInfoSerializer(created_transaction).data, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Get transections",
    description="Get user's transactions",
    methods=["GET"],
    parameters=[
        OpenApiParameter(name="limit", required=True, type=int, default=100),
        OpenApiParameter(name="offset", required=True, type=int, default=0),
        OpenApiParameter(
            name="category_id",
            required=False,
            type=OpenApiTypes.INT,
        ),
    ],
    responses={
        200: OpenApiResponse(response=TransactionInfoSerializer),
        401: OpenApiResponse(description="Error: Authentication credentials were not provided."),
        500: OpenApiResponse(description="Error: Internal server error."),
    },
    tags=[
        "transactions",
    ],
)
@api_view(['GET'])
def get_transactions(request: HttpRequest):
    user_id = request.user.id
    transactions = Transaction.objects.filter(
        user_transaction_for_transaction__user__id=user_id
    ).order_by('-created_at')
    category_id = request.GET.get('category_id')
    if category_id:
        if not UserCategory.objects.filter(id=category_id, user__id=user_id).exists():
            raise exceptions.BadRequest(detail='You do not have category with provided ID.')
        transactions = transactions.filter(category__id=category_id) 

    pagination = LimitOffsetPagination()
    paginated_transactions = pagination.paginate_queryset(transactions, request)
    serializer = TransactionInfoSerializer(paginated_transactions, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Update transection",
    description="Update user's transaction",
    methods=["PUT"],
    request=TransactionUpdateCategorySerializer,
    responses={
        200: OpenApiResponse(response=TransactionSerializer),
        400: OpenApiResponse(description="Error: You do not have category with related ID."),
        401: OpenApiResponse(description="Error: Authentication credentials were not provided."),
        500: OpenApiResponse(description="Error: Internal server error."),
    },
    tags=[
        "transactions",
    ],
)
@api_view(['PUT'])
@transaction.atomic
def update_transaction(request: HttpRequest, transaction_id: int):
    user_id = request.user.id
    data = JSONParser().parse(request)

    transaction = Transaction.objects.get(
        id=transaction_id,
        user_transaction_for_transaction__user__id=user_id
    )
    
    category_id = data['category_id']
    if not UserCategory.objects.filter(user__id=user_id, id=category_id).exists():
        raise exceptions.BadRequest(detail='You do not have category with provided ID.')

    serializer = TransactionUpdateCategorySerializer(
        transaction,
        data=data,
    )
    serializer.is_valid(raise_exception=True)
    updated_transaction = serializer.save()
    return Response(data=TransactionInfoSerializer(updated_transaction).data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Delete transections",
    description="Delete user's transactions",
    methods=["DELETE"],
    parameters=[
        OpenApiParameter(name="limit", required=True, type=int, default=100),
        OpenApiParameter(name="offset", required=True, type=int, default=0),
    ],
    responses={
        204: OpenApiResponse(description="Transaction record was deleted"),
        400: OpenApiResponse(description="Error: You do not have transaction with related ID."),
        401: OpenApiResponse(description="Error: Authentication credentials were not provided."),
        500: OpenApiResponse(description="Error: Internal server error"),
    },
    tags=[
        "transactions",
    ],
)
@api_view(['DELETE'])
def delete_transaction(request: HttpRequest, transaction_id: int):
    try:
        transaction = Transaction.objects.get(
            id=transaction_id,
            user_transaction_for_transaction__user__id=request.user.id,
        )
    except Transaction.DoesNotExist:
        raise exceptions.BadRequest(detail='You do not have transaction with related ID.')
    transaction = transaction.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
