import base64
from datetime import datetime

import structlog
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from django.conf import settings
from pytz import timezone
from rest_framework.views import exception_handler


logger = structlog.getLogger(__name__)


def get_utc_now() -> datetime:
    t = datetime.utcnow()  # Note: despite the method name, this returns a timezone unaware timestamp, hence the conversion below
    tz = timezone('UTC')
    return tz.localize(t)


def status_response(status='OK', msg=None, additional={}):
    if msg:
        additional['msg'] = msg

    additional['Status'] = status

    return additional


# Helper function for determining if request is for csv serialization.
# startswith because browsableapi is sending 'text/csv;q=0.8'
def is_csv_request(request):
    return request.accepted_media_type.startswith('text/csv')


def default_exception_handler(exception, context):
    request = context.get('request', None)
    response = exception_handler(exception, context)
    if request and response:
        if not settings.SUPPRESS_BOUNDARY_EXCEPTION_LOGGING:
            logger.debug('Handled Boundary Exception', exc_info=exception)

        return response

    # Note: Unhandled exceptions will raise a 500 error.
    return None


class AESCipher:
    AES_KEY = pad(settings.AES_KEY.encode(), AES.block_size)
    AES_IV = base64.b64decode(settings.AES_IV.encode())

    def aes_encryption(self, data: str) -> str:
        encoded_data = data.encode()
        padded_encoded_data = pad(encoded_data, AES.block_size)

        cipher = AES.new(self.AES_KEY, AES.MODE_CBC, iv=self.AES_IV)
        cipher_text = cipher.encrypt(padded_encoded_data)
        return base64.b64encode(cipher_text).decode()

    def aes_decryption(self, data: str) -> str:
        data = base64.b64decode(data.encode())

        decrypt_cipher = AES.new(self.AES_KEY, AES.MODE_CBC, self.AES_IV)
        plain_text = decrypt_cipher.decrypt(data)
        return unpad(plain_text, AES.block_size).decode()

