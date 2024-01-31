from django.urls import path

from apiv1.schedule import views

urlpatterns = [
    path('', views.ScheduleOnThisWeekList.as_view(), name='schedule_week_list'),
]
