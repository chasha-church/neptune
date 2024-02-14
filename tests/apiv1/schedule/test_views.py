from django.urls import reverse
from rest_framework import status

from tests.apiv1.schedule.test_api_services import DATA_MOCK
from tests.base import APITestBase
from tools.api.azbykaru.api import AzbykaruAPIClient


class TestScheduleOnThisWeekList(APITestBase):
    view_name = 'schedule_week_list'

    def setUp(self):
        super().setUp()

        api_get_day_mock = self.create_patch_object(AzbykaruAPIClient, 'get_day')
        api_get_day_mock.return_value = DATA_MOCK

    def test_get(self):
        response = self.app.get(reverse(self.view_name,))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json_body)
        self.assertTrue(response.json_body['results'][0]['holidays'][0]['name'])
        self.assertTrue(response.json_body['results'][0]['holidays'][0]['url'])
        self.assertTrue(response.json_body['results'][0]['people'][0]['name'])
        self.assertTrue(response.json_body['results'][0]['people'][0]['url'])
        self.assertListEqual(['title', 'time'], list(response.json_body['results'][6]['events'][0].keys()))
        self.assertTrue(response.json_body['results'][6]['date'])
        self.assertTrue(response.json_body['results'][6]['day_of_week'])

    def test_get_with_week_query_param(self):
        response = self.app.get(reverse(self.view_name,), params={
            'week': 1
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json_body)
