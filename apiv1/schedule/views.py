from datetime import datetime

from django.utils import timezone

from apiv1.generics import NoCacheListAPIView
from apiv1.mixins import RequestArgMixin
from apiv1.pagination import DefaultPageNumberPagination
from apiv1.queryables import Queryable
from apiv1.schedule.serializers import ScheduleOnDayListSerializer
from apiv1.schedule.services import ScheduleService


class ScheduleOnThisWeekList(NoCacheListAPIView, Queryable, RequestArgMixin):
    pagination_class = DefaultPageNumberPagination
    serializer_class = ScheduleOnDayListSerializer

    def get_queryset(self):
        week = self.get_argument('week', required=False, arg_type=int)
        schedule_service = ScheduleService()

        timestamp = datetime.fromisocalendar(datetime.now().year, week, 1) if week else timezone.now()
        return schedule_service.build_schedule(timestamp)
