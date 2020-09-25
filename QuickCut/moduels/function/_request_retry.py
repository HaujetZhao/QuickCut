from functools import wraps
import requests

def _request_retry(*, times=5):
    def decorator(wrapped):
        @wraps(wrapped)
        def wrapper(*args, **kwargs):
            counter = 1
            while counter <= times:
                try:
                    return wrapped(*args, **kwargs)
                except requests.RequestException as e:
                    if counter < times:
                        print(f'{wrapped} failed {counter} time(s): {e}. '
                              f'Retrying')
                    else:
                        print(f'{wrapped} failed {counter} time(s): {e}.')
                        raise
                    counter += 1
        return wrapper
    return decorator

