from datetime import datetime

from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apiv1.mixins import RequestArgMixin
from apiv1.pagination import DefaultPageNumberPagination
from apiv1.queryables import Queryable
from apiv1.schedule.serializers import ScheduleOnDayListSerializer
from apiv1.schedule.services import ScheduleService
from tools.cors.decorators import allow_cors, allow_cors_methods, cors_max_age


class ScheduleOnThisWeekList(GenericAPIView, Queryable, RequestArgMixin):
    pagination_class = DefaultPageNumberPagination
    serializer_class = ScheduleOnDayListSerializer

    def get_queryset(self):
        return None

    @allow_cors(settings.CORS)
    @allow_cors_methods(settings.CORS_METHODS)
    @cors_max_age(settings.CORS_MAX_AGE)
    def get(self, request, *args, **kwargs):
        week = self.get_argument('week', required=False, arg_type=int)
        schedule_service = ScheduleService()

        timestamp = datetime.fromisocalendar(datetime.now().year, week, 1) if week else timezone.now()
        data = schedule_service.build_schedule(timestamp)

        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
