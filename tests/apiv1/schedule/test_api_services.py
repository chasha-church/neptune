from datetime import datetime

from apiv1.schedule.api_services import AzbykaruAPIClientAdapter
from tests.base import APITestBase
from tools.api.azbykaru.api import AzbykaruAPIClient

DATA_MOCK = [
    {
        "abstractDate": {
            "priorities": [
                {
                    "paragraph": 1,
                    "number": 0,
                    "memorialDay": {
                        "cacheTitle": '<a href="http://azbyka.ru/days/prazdnik-svjatoe-bogojavlenie-kreshchenie-'
                                      'gospoda-boga-i-spasa-nashego-iisusa-hrista">Попразднство Богоявления</a>',
                        "holidayAdditionalDay": {"title": "Попразднство Богоявления"},
                    },
                },
                {
                    "paragraph": 1,
                    "number": 1,
                    "memorialDay": {
                        "cacheTitle": '<a href="https://azbyka.ru/days/sv-polievkt-melitinskij">'
                                      'Мч. Полие́вкта Мелитинского (259)</a>'
                    },
                },
                {
                    "paragraph": 1,
                    "number": 2,
                    "memorialDay": {
                        "cacheTitle": '<a href="https://azbyka.ru/days/sv-filipp-II-moskovskij-i-vseja-rusi"><strong>'
                                      'святителя Фили́ппа, митрополита Московского и всея России, чудотворца (1569)'
                                      '</strong></a>'
                    },
                },
                {
                    "paragraph": 2,
                    "number": 1,
                    "memorialDay": {
                        "cacheTitle": '<a href="http://azbyka.ru/days/sv-iona-kievskij-miroshnichenko">Прп. Ио́ны '
                                      '(в схиме Петра́) Киевского (1902)</a>'
                    },
                },
                {
                    "paragraph": 2,
                    "number": 3,
                    "memorialDay": {
                        "cacheTitle": '<a href="http://azbyka.ru/days/sv-petr-sevastijskij">свт. Петра, епископа '
                                      'Севастии Армянской (IV)</a>'
                    },
                },
                {
                    "paragraph": 2,
                    "number": 2,
                    "memorialDay": {
                        "cacheTitle": '<a href="http://azbyka.ru/days/sv-samej">прор. Саме́я (X в. до Р. Х.)</a>'
                    },
                },
                {
                    "paragraph": 2,
                    "number": 4,
                    "memorialDay": {
                        "cacheTitle": '<a href="http://azbyka.ru/days/sv-evstratij-tarsijskij">прп. Евстра́тия '
                                      'Тарсийского, чудотворца, игумена (IX)</a>'
                    },
                },
                {
                    "paragraph": 3,
                    "number": 1,
                    "memorialDay": {
                        "cacheTitle": '<a href="http://azbyka.ru/days/sv-pavel-nikolskij">Сщмч. Павла <span '
                                      'style="font-size: 10pt;"><em>Никольского</em></span>, пресвитера (1943)</a>'
                    },
                },
            ]
        }
    },
    {"abstractDate": {"priorities": []}},
    {"abstractDate": {"priorities": []}},
]


class TestAzbykaruAPIClientAdapter(APITestBase):
    adapter = AzbykaruAPIClientAdapter

    def setUp(self):
        super().setUp()

        api_get_day_mock = self.create_patch_object(AzbykaruAPIClient, 'get_day')
        api_get_day_mock.return_value = DATA_MOCK

    def test_get_day(self):
        response_data = self.adapter().get_day(datetime.now())

        assert response_data.get('holidays')[0].get('name')
        assert response_data.get('holidays')[0].get('url')

        assert response_data.get('people')[0].get('name')
        assert response_data.get('people')[0].get('url')

    def test_get_schedule(self):
        response_data = self.adapter().get_schedule(datetime.now())

        assert len(response_data) == 7

        assert response_data[0].get('holidays')[0].get('name')
        assert response_data[0].get('holidays')[0].get('url')

        assert response_data[0].get('people')[0].get('name')
        assert response_data[0].get('people')[0].get('url')
