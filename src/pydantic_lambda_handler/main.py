"""
The main class which you import and use a decorator.
"""
import functools
from collections import defaultdict
from http import HTTPStatus
from inspect import signature
from typing import Union

from orjson import orjson  # type: ignore

from src.pydantic_lambda_handler.models import BaseOutput


class PydanticLambdaHander:
    """
    The decorator handle.
    """

    def __init__(self, *, title, version=None):
        self.title = title
        self.version = version
        self.paths = defaultdict(dict)

    def get(self, url, *, status_code: Union[HTTPStatus, int] = HTTPStatus.OK):
        """Expect request with a GET method.

        :param url:
        :param status_code:
        :return:
        """
        open_api_status_code = str(int(status_code))
        self.paths[url]["get"] = {
            "responses": {
                open_api_status_code: {"content": {"application/json": {}}, "description": "Successful Response"}
            }
        }

        def create_response(func):
            @functools.wraps(func)
            def wrapper_decorator(event, context):
                sig = signature(func)

                func_args = []
                func_kwargs = {}
                if sig.parameters:
                    path_parameters = event.get("pathParameters", {}) or {}
                    for param, param_info in sig.parameters.items():

                        path_param = path_parameters.get(param)

                        if param_info.annotation == param_info.empty:
                            func_args.append(path_param)
                        else:
                            try:
                                func_args.append(param_info.annotation(path_param))
                            except ValueError:
                                response = BaseOutput(body="", status_code=422)
                                return orjson.loads(response.json())

                    # Do something before
                    body = func(*func_args, **func_kwargs)
                else:
                    body = func()

                response = BaseOutput(body=body, status_code=status_code)
                return orjson.loads(response.json())

            return wrapper_decorator

        return create_response

    def post(self, url, *, status_code: Union[HTTPStatus, int] = HTTPStatus.CREATED):
        """Expect request with a POST method.

        :param url:
        :param status_code:
        :return:
        """
        open_api_status_code = str(int(status_code))
        self.paths[url]["post"] = {
            "responses": {
                open_api_status_code: {"content": {"application/json": {}}, "description": "Successful Response"}
            }
        }

        def create_response(func):
            @functools.wraps(func)
            def wrapper_decorator(event, context):
                sig = signature(func)

                func_args = []
                func_kwargs = {}
                if sig.parameters:
                    path_parameters = event.get("pathParameters", {}) or {}
                    for param, param_info in sig.parameters.items():

                        path_param = path_parameters.get(param)

                        if param_info.annotation == param_info.empty:
                            func_args.append(path_param)
                        else:
                            try:
                                func_args.append(param_info.annotation(path_param))
                            except ValueError:
                                response = BaseOutput(body="", status_code=422)
                                return orjson.loads(response.json())

                    # Do something before
                    body = func(*func_args, **func_kwargs)
                else:
                    body = func()

                response = BaseOutput(body=body, status_code=status_code)
                return orjson.loads(response.json())

            return wrapper_decorator

        return create_response

    def generate_open_api(self):
        open_api = {
            "openapi": "3.0.2",
            "info": {"title": self.title, "version": self.version},
            "paths": dict(self.paths),
        }
        return open_api
