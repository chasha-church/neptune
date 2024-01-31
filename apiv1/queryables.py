from django.conf import settings


class Queryable:
    customer_domain = settings.CUSTOMER_DOMAIN

    def qs(self, model):
        return model.objects.using(self.customer_domain)

    def create_object(self, model, **kwargs):
        return self.qs(model).create(**kwargs)
