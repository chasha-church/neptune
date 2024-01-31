from requests import ConnectTimeout, HTTPError

from tools.api.azbykaru.exceptions import AzbykaruConnectionError, AzbykaruCredentialsError


def token_checker(login_func):
    """Decorator that handles connection executions and login if needed."""
    def decorator(function):
        def wrapper(self, *args, **kwargs):
            result = exception_handler(None, function, *[self, *args], **kwargs)
            if result:
                return result

            login_response = exception_handler(AzbykaruCredentialsError, login_func, self)
            if login_response:
                return exception_handler(AzbykaruConnectionError, function, *[self, *args], **kwargs)

        return wrapper

    def exception_handler(exception, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (HTTPError, ConnectTimeout, ConnectionError) as e:
            if exception:
                raise exception(e)
    return decorator


def exception_checker(func):
    '''Decorator that handles Zoom connection executions.'''

    def wrap(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except HTTPError as e:
            raise AzbykaruCredentialsError
        except (ConnectTimeout, ConnectionError) as e:
            raise AzbykaruConnectionError
        return result

    return wrap
