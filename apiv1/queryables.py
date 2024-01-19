class Queryable:
    customer_domain = 'develop'

    def qs(self, model):
        return model.objects.using(self.customer_domain)

    def create_object(self, model, **kwargs):
        return self.qs(model).create(**kwargs)
