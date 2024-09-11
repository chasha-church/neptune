from datetime import datetime
from typing import Dict

from django.conf import settings

from tools.api.azbykaru.services import SourceService
from .communications.http import HTTPMethods
from .utils import token_checker
from ...standard.api_client import APIClient


class BaseAPIClient(APIClient):
    def __init__(self):
        self.source_service = SourceService()
        self._access_token = self.source_service.get_token() or ''
        super(BaseAPIClient, self).__init__(communication=HTTPMethods,
                                            credential={"email": settings.AZBYKARU_API_LOGIN,
                                                        "password": settings.AZBYKARU_API_PASSWORD})

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    def post(self, resource, headers, body):
        uri = settings.AZBYKARU_BASE_URL + resource
        all_headers = self.communication.build_headers(self._access_token)
        if headers:
            all_headers.update(headers)
        return self.communication.post(self, uri, headers=all_headers, body=body)

    def get(self, resource, headers, query_params, base_url=settings.AZBYKARU_BASE_URL):
        uri = base_url + resource
        all_headers = self.communication.build_headers(self._access_token)
        if headers:
            all_headers.update(headers)
        return self.communication.get(self, uri, headers=all_headers, query_params=query_params)

    def delete(self, resource, headers):
        uri = settings.AZBYKARU_BASE_URL + resource
        all_headers = self.communication.build_headers(self._access_token)
        if headers:
            all_headers.update(headers)
        return self.communication.delete(self, uri, headers=all_headers)

    def head(self, resource, headers):
        uri = settings.AZBYKARU_BASE_URL + resource
        all_headers = self.communication.build_headers(self._access_token)
        if headers:
            all_headers.update(headers)
        return self.communication.head(self, uri, headers=all_headers)


class AzbykaruAPIClient(BaseAPIClient):
    LOGIN_URL = 'login'
    DAY_URL = 'day'

    def login(self):
        response = self.post(self.LOGIN_URL, headers={}, body=self.credential)

        if response:
            self._access_token = response.get('token')
            self.source_service.set_token(self._access_token)

    @token_checker(login)
    def get_day(self, timestamp: datetime) -> Dict:
        query_params = {'date[exact]': str(timestamp.date())}
        response_data = self.get(self.DAY_URL, headers={}, query_params=query_params)
        return response_data
