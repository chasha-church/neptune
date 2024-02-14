from datetime import time, datetime, timedelta
from typing import List, Optional, Dict

from bs4 import BeautifulSoup

from tools.api.azbykaru.api import AzbykaruAPIClient


class AzbykaruAPIClientAdapter(AzbykaruAPIClient):
    DAY_OF_WEEK_MAP = {
        1: 'понедельник',
        2: 'вторник',
        3: 'среда',
        4: 'четверг',
        5: 'пятница',
        6: 'суббота',
        7: 'воскресенье',
    }
    DATE_ATTRIBUTE_NAME = 'date'
    DAY_OF_WEEK_ATTRIBUTE_NAME = 'day_of_week'

    def _parse_day_item(self, text: str) -> Optional[Dict]:
        if text:
            soup = BeautifulSoup(text, 'html.parser')
            return {'name': ' '.join(soup.stripped_strings),
                    'url': next(tag.attrs.get('href') for tag in soup.findAll('a'))}

    def get_day(self, timestamp: datetime) -> Dict:
        data = super().get_day(timestamp)
        day_data_list = (abstract_data.get('abstractDate', {}).get('priorities') for abstract_data in data)
        result_data = {'holidays': [], 'people': []}

        for priorities_list in day_data_list:
            for day_item in (item.get('memorialDay', {}) for item in priorities_list):
                parsed_day_item_data = self._parse_day_item(day_item.get('cacheTitle'))

                if not parsed_day_item_data:
                    continue

                if 'holiday' in day_item or 'holidayAdditionalDay' in day_item:
                    result_data['holidays'].append(parsed_day_item_data)
                else:
                    result_data['people'].append(parsed_day_item_data)

        return result_data

    def get_schedule(self, timestamp: datetime) -> Optional[List[dict]]:
        timestamp = timestamp or datetime.utcnow()

        year_weeknumber_weekday = list(timestamp.isocalendar())
        result_data = []

        for weekday in range(1, 7 + 1):
            year_weeknumber_weekday[2] = weekday
            day_timestamp = datetime.fromisocalendar(*year_weeknumber_weekday)

            day_data = self.get_day(day_timestamp)
            day_data[self.DATE_ATTRIBUTE_NAME] = day_timestamp.date()
            day_data[self.DAY_OF_WEEK_ATTRIBUTE_NAME] = self.DAY_OF_WEEK_MAP[weekday]

            result_data.append(day_data)
        return result_data
