from rest_framework import status
from rest_framework.exceptions import APIException


class AzbykaruCredentialsError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Bad credentials.'


class AzbykaruConnectionError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'The azbyka.ru platform is unavailable'


class AzbykaruMaxRetriesExceededError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'The azbyka.ru platform is unavailable due to too many request retries.'
