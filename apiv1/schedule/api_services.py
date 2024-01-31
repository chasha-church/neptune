from datetime import datetime
from typing import List, Optional, Dict

from bs4 import BeautifulSoup

from tools.api.azbykaru.api import AzbykaruAPIClient


class AzbykaruAPIClientAdapter(AzbykaruAPIClient):
    def _parse_day(self, text: str) -> Optional[Dict]:
        if text:
            soup = BeautifulSoup(text, 'html.parser')
            return {'name': next(soup.stripped_strings),
                    'url': next(tag.attrs.get('href') for tag in soup.findAll('a'))}

    def get_day(self, timestamp: datetime) -> Dict:
        data = super().get_day(timestamp)
        day_data_list = (abstract_data.get('abstractDate', {}).get('priorities') for abstract_data in data)
        result_data = {'holidays': [], 'people': []}

        for priorities_list in day_data_list:
            for day in (item.get('memorialDay', {}) for item in priorities_list):
                parsed_day_data = self._parse_day(day.get('cacheTitle'))

                if not parsed_day_data:
                    continue

                if 'holiday' in day or 'holidayAdditionalDay' in day:
                    result_data['holidays'].append(parsed_day_data)
                else:
                    result_data['people'].append(parsed_day_data)

        return result_data

    def get_schedule(self, timestamp: datetime = None) -> Optional[List[dict]]:
        if timestamp:
            year_weeknumber_weekday = list(timestamp.isocalendar())
            result_data = []

            for weekday in range(1, 7 + 1):
                year_weeknumber_weekday[2] = weekday
                day_timestamp = datetime.fromisocalendar(*year_weeknumber_weekday)

                result_data.append(self.get_day(day_timestamp))

            return result_data
