from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def healthcheck(request: HttpRequest):
    return Response(data={'message': 'OK'})
