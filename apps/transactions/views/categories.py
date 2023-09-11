from django.http import HttpRequest
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status

from ..models import UserCategory
from ..serialiers import CategorySerializer
from extentions import exceptions


@extend_schema(
    summary="Create transaction categories",
    description="Create user's transaction categories",
    methods=["POST"],
    request=CategorySerializer,
    responses={
        201: OpenApiResponse(response=CategorySerializer),
        401: OpenApiResponse(description="Error: Authentication credentials were not provided."),
        500: OpenApiResponse(description="Error: Internal server error."),
    },
    tags=[
        "categories",
    ],
)
@api_view(['POST'])
def create_transaction_category(request: HttpRequest):
    data = JSONParser().parse(request)
    serializer = CategorySerializer(data=data, context={'user_id': request.user.id})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Update transection category",
    description="Update user's transaction category",
    methods=["PUT"],
    request=CategorySerializer,
    responses={
        200: OpenApiResponse(response=CategorySerializer),
        400: OpenApiResponse(description="Error: You do not have category with related ID."),
        401: OpenApiResponse(description="Error: Authentication credentials were not provided."),
        500: OpenApiResponse(description="Error: Internal server error."),
    },
    tags=[
        "categories",
    ],
)
@api_view(['PUT'])
# @transaction.atomic
def update_transaction_category(request: HttpRequest, transaction_category_id: int):
    user_id = request.user.id
    data = JSONParser().parse(request)
    try:
        category = UserCategory.objects.get(
            id=transaction_category_id,
            user__id=user_id
        )
    except UserCategory.DoesNotExist:
        raise exceptions.BadRequest(detail='You do not have category with related ID.')

    serializer = CategorySerializer(
        category,
        data=data,
    )
    serializer.is_valid(raise_exception=True)
    updated_category = serializer.save()
    return Response(data=CategorySerializer(updated_category).data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Get transaction categories",
    description="Get user's transaction categories",
    methods=["GET"],
    parameters=[
        OpenApiParameter(name="limit", required=True, type=int, default=100),
        OpenApiParameter(name="offset", required=True, type=int, default=0),
    ],
    responses={
        200: OpenApiResponse(response=CategorySerializer(many=True)),
        401: OpenApiResponse(description="Error: Authentication credentials were not provided."),
        500: OpenApiResponse(description="Error: Internal server error."),
    },
    tags=[
        "categories",
    ],
)
@api_view(['GET'])
def get_transaction_categories(request: HttpRequest):
    categories = UserCategory.objects.filter(user__id=request.user.id)
    pagination = LimitOffsetPagination()
    paginated_categories = pagination.paginate_queryset(categories, request)
    serializer = CategorySerializer(paginated_categories, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Delete transaction categories",
    description="Delete user's transaction categories",
    methods=["DELETE"],
    request=None,
    responses={
        204: OpenApiResponse(description="Transaction category record was deleted"),
        400: OpenApiResponse(description="Error: You do not have category with related ID."),
        401: OpenApiResponse(description="Error: Authentication credentials were not provided."),
        500: OpenApiResponse(description="Error: Internal server error."),
    },
    tags=[
        "categories",
    ],
)
@api_view(['DELETE'])
def delete_transaction_categories(request: HttpRequest, transaction_category_id: int):
    try:
        category = UserCategory.objects.filter(
            id=transaction_category_id,
            user__id=request.user.id,
        )
    except UserCategory.DoesNotExist:
        raise exceptions.BadRequest(detail='You do not have category with related ID.')
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
   