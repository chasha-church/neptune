from datetime import datetime

import factory
from django.conf import settings

from db import models


class MyFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        abstract = True

    @classmethod
    def _get_manager(cls, model_class):
        return model_class.objects.using(settings.TEST_CUSTOMER_DOMAIN)

    @classmethod
    def all(cls):
        return cls._get_manager(cls._meta.model).all()

    @classmethod
    def none(cls):
        return cls._get_manager(cls._meta.model).none()

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls._get_manager(cls._meta.model).filter(*args, **kwargs)

    @classmethod
    def truncate(cls):
        cls._get_manager(cls._meta.model).delete()


class CreatedUpdatedMyFactory(MyFactory):
    created_by_id = 1
    created_date = factory.LazyFunction(datetime.utcnow)
    updated_by_id = 1
    updated_date = factory.LazyFunction(datetime.utcnow)


class AssetsFactory(CreatedUpdatedMyFactory):
    class Meta:
        model = models.Assets

    file_name = 'file_name.png'


class NewsContentFactory(CreatedUpdatedMyFactory):
    class Meta:
        model = models.NewsContent

    title = 'Default Title'
    text = 'Default Text'
    main_asset = factory.SubFactory(AssetsFactory)
    assets = factory.SubFactory(AssetsFactory)

    @factory.post_generation
    def assets(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.assets.add(*extracted)


class NewsContentAssets(MyFactory):
    class Meta:
        model = models.NewsContentAssets

    news_content = factory.SubFactory(NewsContentFactory)
    asset = factory.SubFactory(AssetsFactory)
