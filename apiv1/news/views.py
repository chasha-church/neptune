from apiv1 import generics
from apiv1.news import serializers
from apiv1.pagination import DefaultPageNumberPagination
from apiv1.queryables import Queryable
from db import models


class NewsList(generics.NoCacheListAPIView, Queryable):
    serializer_class = serializers.NewsListSerializer
    pagination_class = DefaultPageNumberPagination

    def get_queryset(self):
        return self.qs(models.NewsContent).order_by('-created_date').all()


class NewsDetails(generics.NoCacheRetrieveCreateAPIView, Queryable):
    serializer_class = serializers.NewsDetailsSerializer
    pagination_class = DefaultPageNumberPagination

    def get_queryset(self):
        return self.qs(models.NewsContent).prefetch_related('assets').order_by('-updated_date').all()
