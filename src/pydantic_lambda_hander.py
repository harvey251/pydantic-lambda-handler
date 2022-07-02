"""
The main class which you import and use a decorator.
"""
import functools
from http import HTTPStatus
from inspect import signature
from typing import Union

from orjson import orjson

from src.models import BaseOutput


class PydanticLambdaHander:
    """
    The decorator handle.
    """

    @classmethod
    def get(cls, url, *, status_code: Union[HTTPStatus, int] = HTTPStatus.OK):
        """Expect request with a GET method.

        :param url:
        :param status_code:
        :return:
        """

        def create_response(func):
            @functools.wraps(func)
            def wrapper_decorator(*args, **kwargs):

                sig = signature(func)
                if sig.parameters:
                    raise NotImplementedError
                    # Do something before
                    body = func(*args, **kwargs)
                else:
                    body = func()

                response = BaseOutput(body=body, status_code=status_code)
                return orjson.loads(response.json())

            return wrapper_decorator

        return create_response
