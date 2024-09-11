from typing import Optional

from apiv1.queryables import Queryable
from apiv1.utils import AESCipher
from db.sources import models
from django.conf import settings


class SourceService(Queryable):
    SOURCE_NAME = 'Azbukaru'
    SOURCE_ATTR_NAME = f'{SOURCE_NAME}.AccessToken'

    def __init__(self) -> None:
        self.source= self._get_or_create_source()
        self.aes_cipher = AESCipher()

    def get_token(self) -> Optional[str]:
        source_attr = self._get_access_token()
        if source_attr:
            return self.aes_cipher.aes_decryption(source_attr.value)

    def _get_access_token(self) -> Optional[models.SourceAttributes]:
        return self.qs(models.SourceAttributes).filter(source=self.source, key=self.SOURCE_ATTR_NAME).first()

    def _get_or_create_source(self) -> models.Source:
        source = self.qs(models.Source).filter(name=self.SOURCE_NAME).last()

        if source:
            return source

        return self.qs(models.Source).create(
            name=self.SOURCE_NAME,
            login=settings.AZBYKARU_API_LOGIN,
            password=settings.AZBYKARU_API_PASSWORD,
        )

    def set_token(self, token: str) -> None:
        encrypted_token = self.aes_cipher.aes_encryption(token)
        self.qs(models.SourceAttributes).update_or_create(source=self.source, key=self.SOURCE_ATTR_NAME,
                                                          defaults={'value': encrypted_token})

    def get_source_attr(self) -> Optional[models.SourceAttributes]:
        return self.qs(models.SourceAttributes).filter(source=self.source, key=self.SOURCE_ATTR_NAME).first()
