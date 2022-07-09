"""
The main class which you import and use a decorator.
"""
import functools
import re
from collections import defaultdict
from http import HTTPStatus
from inspect import signature
from typing import Union

from orjson import orjson  # type: ignore
from pydantic import ValidationError, create_model

from pydantic_lambda_handler.models import BaseOutput


class PydanticLambdaHandler:
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
            "responses": {open_api_status_code: {"content": {"application/json": {}}}},
            "operationId": "GET HTTP",
        }

        def create_response(func):
            sig = signature(func)

            if sig.parameters:
                model_dict = {}
                for param, param_info in sig.parameters.items():
                    if param_info.default != param_info.empty:
                        raise ValueError("Should not set default for path parameters")

                    if param_info.annotation == param_info.empty:
                        model_dict[param] = str, ...
                    else:
                        model_dict[param] = param_info.annotation, ...

                path_parameters = set(re.findall(r"\{(.*?)\}", url))

                if path_parameters != set(model_dict.keys()):
                    raise ValueError("Missing path parameters")

                PathModel = create_model("PathModel", **model_dict)

                path_schema_initial = PathModel.schema()
                properties = []
                for name, property_info in path_schema_initial.get("properties", {}).items():
                    #  {"name": "petId", "in": "path", "required": True, "schema": {"type": "string"}}
                    p = {"name": name, "in": "path", "schema": {"type": property_info.get("type", "string")}}
                    if name in path_schema_initial.get("required", ()):
                        p["required"] = True

                    properties.append(p)

                self.paths[url]["get"]["parameters"] = properties

                EventModel = create_model("EventModel", path=(PathModel, {}))

            @functools.wraps(func)
            def wrapper_decorator(event, context):
                if sig.parameters:
                    path_parameters = event.get("pathParameters", {}) or {}

                    try:
                        event = EventModel(path=path_parameters)
                    except ValidationError as e:
                        response = BaseOutput(
                            body={"detail": orjson.loads(e.json())}, status_code=HTTPStatus.UNPROCESSABLE_ENTITY
                        )
                        return orjson.loads(response.json())

                    # Do something before
                    body = func(**event.path.dict())
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
        """
        https://stackoverflow.com/questions/5910703/how-to-get-all-methods-of-a-python-class-with-given-decorator
        :return:
        """
        open_api = {
            "openapi": "3.0.2",
            "info": {"title": self.title, "version": self.version},
            "paths": dict(self.paths),
        }

        # TODO: move out into a seperate module
        # folder_dir = Path(__file__).parent
        # inspect.getmodule()
        return open_api
