from django.urls import reverse
from rest_framework import status

from tests.base import APITestBase


class TestNewsList(APITestBase):
    view_name = 'news_list'

    def test_get(self):
        response = self.app.get(reverse(self.view_name,))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json_body)
