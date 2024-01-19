from django.apps import apps
from django.conf import settings
from django.db import connections


class TestDatabasesShim(dict):

    def __getitem__(self, key):
        key = str(key)

        if key in self:
            return super().__getitem__(key)

        self[key] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '%s/%s' % (settings.DATABASE_PATH, key,),
        }

        with connections[key].schema_editor() as schema_editor:
            for model in filter(lambda model:model.__module__.startswith('db'), apps.get_models()):
                schema_editor.create_model(model)

        return self[key]


class TestSFMasterRouter(object):
    def _default_db(self, model):
        if model._meta.app_label == 'db':
            return settings.CUSTOMER_DOMAIN
        return 'default'

    def db_for_read(self, model, **hints):
        db = getattr(getattr(hints.get("instance", None), "_state", None), "db", None)
        if db:
            return db
        return self._default_db(model)

    def db_for_write(self, model, **hints):
        db = getattr(getattr(hints.get("instance", None), "_state", None), "db", None)
        if db:
            return db
        return self._default_db(model)

    def allow_relation(self, obj1, obj2):
        return True

    def allow_migrate(self, db, app_label, model=None, **hints):
        if model and model.__module__.startswith('sfdb.sfcontroller') and db != 'sfcontroller':
            return False
        if model and model.__module__.startswith('sfdb.sfcustomer') and db != 'sfcustomer':
            return False


def add_column_to_table(using, table_name, column_name, column_type):
    query = "ALTER TABLE '%s' ADD COLUMN '%s' %s NULL" % (
        table_name, column_name, column_type)
    cursor = connections[using].cursor()
    cursor.execute(query)
