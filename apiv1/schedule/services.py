from datetime import datetime, time
from typing import List, Dict

from apiv1.schedule.api_services import AzbykaruAPIClientAdapter


class ScheduleService:
    DEFAULT_EVENTS_DATA_PER_WEEK = [
        {
            'events': None
        },
        {
            'events': [
                {
                    'title': 'Вечерня. Утреня. 1-ый час',
                    'time': time(18, 0)
                },
            ]
        },

        {
            'events': [
                {
                    'title': 'Литургия',
                    'time': time(9, 0)
                },
            ]
        },
        {
            'events': None
        },
        {
            'events': [
                {
                    'title': 'Вечерня. Утреня. 1-ый час',
                    'time': time(18, 0)
                },
            ]
        },
        {
            'events': [
                {
                    'title': 'Литургия',
                    'time': time(9, 0)
                },
                {
                    'title': 'Всенощное Бдение',
                    'time': time(18, 0)
                },
            ]
        },
        {
            'events': [
                {
                    'title': 'Литургия',
                    'time': time(9, 0)
                },
                {
                    'title': 'Молебен с Акафистом Божией Матери в честь иконы Ея "Неупиваемая Чаша',
                    'time': time(18, 0)
                },
                {
                    'title': 'Беседы перед Таинством Крещения',
                    'time': time(19, 0)
                },
            ]
        },
    ]

    def build_schedule(self, timestamp: datetime):
        holiday_people_data = AzbykaruAPIClientAdapter().get_schedule(timestamp)
        return self._add_events_data(holiday_people_data)

    def _add_events_data(self, week_data: List[Dict]) -> List[Dict]:
        for day_data, additional_data in zip(week_data, self.DEFAULT_EVENTS_DATA_PER_WEEK):
            day_data.update(additional_data)

        return week_data
