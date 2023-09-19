from rest_framework.exceptions import APIException


class AlreadyExist(APIException):
    status_code = 400
    default_detail = "Already exist"
    default_code = "already_exist"


class BadRequest(APIException):
    status_code = 400
    default_detail = "Bad request"
    default_code = "bad_request"
