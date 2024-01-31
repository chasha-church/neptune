from datetime import datetime

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from apiv1 import generics
from apiv1.mixins import RequestArgMixin
from apiv1.pagination import DefaultPageNumberPagination
from apiv1.queryables import Queryable
from apiv1.schedule.api_services import AzbykaruAPIClientAdapter


class ScheduleOnThisWeekList(generics.NoCacheListAPIView, Queryable, RequestArgMixin):
    pagination_class = DefaultPageNumberPagination

    def get(self, request, *args, **kwargs):
        week = self.get_argument('week', required=False, arg_type=int)
        schedule_service = AzbykaruAPIClientAdapter()

        if week:
            data = schedule_service.get_schedule(datetime.fromisocalendar(datetime.now().year, week, 1))
        else:
            data = schedule_service.get_schedule(timezone.now())
        return Response(data, status=status.HTTP_200_OK)
