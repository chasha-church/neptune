from rest_framework import status
from rest_framework.exceptions import APIException


class AzbykaruCredentialsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad credentials.'


class AzbykaruConnectionError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The azbyka.ru platform is unavailable'
