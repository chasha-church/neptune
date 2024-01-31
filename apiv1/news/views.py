from apiv1 import generics
from apiv1.news.serializers import NewsListSerializer
from apiv1.pagination import DefaultPageNumberPagination
from apiv1.queryables import Queryable
from db import models


class NewsList(generics.NoCacheListAPIView, Queryable):
    serializer_class = NewsListSerializer
    pagination_class = DefaultPageNumberPagination

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return self.qs(models.NewsContent).prefetch_related('assets').order_by('-updated_date').all()
