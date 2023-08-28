from rest_framework import views
from rest_framework.response import Response

from apiv1.news.contracts import news_content_contract


class NewsList(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response(news_content_contract)
