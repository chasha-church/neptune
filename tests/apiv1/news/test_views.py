from django.urls import reverse
from rest_framework import status

from apiv1.queryables import Queryable
from tests import factories
from tests.base import APITestBase


class TestNewsList(APITestBase, Queryable):
    view_name = 'news_list'

    def setUp(self):
        super().setUp()
        self.asset = factories.AssetsFactory()
        self.news = factories.NewsContentFactory(assets=(self.asset,))

    def test_get(self):
        response = self.app.get(reverse(self.view_name,))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertSetEqual(
            set(response.json_body['results'][0].keys()),
            {'news_content_id', 'title', 'main_asset_url', 'created_date',
             'created_by_id', 'updated_date', 'updated_by_id'})


class TestNewsDetails(APITestBase):
    view_name = 'news_details'

    def setUp(self):
        super().setUp()
        self.asset = factories.AssetsFactory()
        self.news = factories.NewsContentFactory(assets=(self.asset,))

    def test_get(self):
        response = self.app.get(reverse(self.view_name, args=(self.news.pk,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertSetEqual(
            set(response.json_body.keys()),
            {'news_content_id', 'title', 'main_asset_url', 'created_date',
             'created_by_id', 'updated_date', 'updated_by_id', 'text', 'view_data', 'assets_url'})
