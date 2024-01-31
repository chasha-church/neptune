from rest_framework import serializers


class HolidayOrPeopleObjectSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.CharField()


class EventSerializer(serializers.Serializer):
    title = serializers.CharField()
    time = serializers.TimeField(format='%H:%M')


class ScheduleOnDayListSerializer(serializers.Serializer):

    holidays = HolidayOrPeopleObjectSerializer(many=True)
    people = HolidayOrPeopleObjectSerializer(many=True)
    events = EventSerializer(many=True)
