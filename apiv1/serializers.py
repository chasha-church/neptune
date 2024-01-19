import functools
from datetime import date

from apiv1.utils import get_utc_now
from db import models
from db.utils import get_user_info_from_request


class AutoUpdateMixinBase(object):

    def get_auto_fields(self, action):
        return {}

    def update(self, instance, validated_data):
        validated_data = self.update_fields('update', validated_data)
        return super(AutoUpdateMixinBase, self).update(instance, validated_data)

    def update_fields(self, action, validated_data):
        for fields, get_auto_value in self.get_auto_fields(action).items():
            value = getattr(self, get_auto_value)()
            validated_data.update(dict((field, value) for field in fields if field))

        return validated_data


class ListAutoUpdateMixin(AutoUpdateMixinBase):
    def update_fields(self, action, validated_data):
        for fields, get_auto_value in self.get_auto_fields(action).items():
            value = getattr(self, get_auto_value)()
            for item in validated_data:
                item.update(dict((field, value) for field in fields if field))
        return validated_data


class AutoNowMixin(AutoUpdateMixinBase):
    created_date_field = 'created_date'
    updated_date_field = 'updated_date'

    def get_auto_fields(self, action):
        auto_fields_map = {
            'create': {(self.created_date_field, self.updated_date_field): 'get_now'},
            'update': {(self.updated_date_field,): 'get_now'}
        }
        auto_fields = super(AutoNowMixin, self).get_auto_fields(action)
        auto_fields.update(auto_fields_map.get(action, {}))

        return auto_fields

    def get_now(self):
        return get_utc_now()

    def get_today(self):
        return date.today()


class UserMixin:
    @functools.lru_cache(maxsize=None)
    def get_user(self):
        username, domain = get_user_info_from_request(self.context['request'])
        return models.User.objects.using(domain).get(user_name=username)


class AutoUserMixin(UserMixin, AutoUpdateMixinBase):
    created_by_field = 'created_by_id'
    updated_by_field = 'updated_by_id'

    def get_auto_fields(self, action):
        auto_fields = super(AutoUserMixin, self).get_auto_fields(action)

        auto_fields_map = {
            'create': {(self.created_by_field, self.updated_by_field): 'get_user_pk'},
            'update': {(self.updated_by_field,): 'get_user_pk'}
        }

        auto_fields.update(auto_fields_map.get(action, {}))

        return auto_fields
