from datetime import datetime

import structlog
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
