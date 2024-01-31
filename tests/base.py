from unittest import mock

from django.core.cache import cache
from django_webtest import WebTest


class APITestBase(WebTest):
    def setUp(self):
        self.auth_mock = self.create_patch('rest_framework.views.APIView.check_permissions')
        self.auth_mock.return_value = True

        super(APITestBase, self).setUp()

    def tearDown(self):
        # Flush cached schema data.
        cache.clear()

    def start_patch(self, patcher):
        mock_instance = patcher.start()
        self.addCleanup(patcher.stop)
        return mock_instance

    def create_patch(self, path, **kwargs):
        patcher = mock.patch(path, **kwargs)
        return self.start_patch(patcher)

    def create_patcher(self, func_path, **kwargs):
        return mock.patch(func_path, **kwargs)

    def create_patch_object(self, obj, path, **kwargs):
        patcher = mock.patch.object(obj, path, **kwargs)
        return self.start_patch(patcher)

    def exception_side_effect(self, *items):
        generator = (item for item in items)

        def effect(*args, **kwargs):
            try:
                exception, message = next(generator)
                raise exception(message)
            except StopIteration:
                return None

        return effect
