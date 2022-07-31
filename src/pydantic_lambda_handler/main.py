"""
The main class which you import and use a decorator.
"""
import functools
import json
import re
from collections import defaultdict
from http import HTTPStatus
from inspect import signature
from typing import Union

from pydantic import ValidationError, create_model

from pydantic_lambda_handler.models import BaseOutput


class PydanticLambdaHandler:
    """
    The decorator handle.
    """

    def __init__(self, *, title="PydanticLambdaHandler", version="0.0.0"):
        self.title = title
        self.version = version
        self.paths = defaultdict(dict)

    def get(
        self,
        url,
        *,
        status_code: Union[HTTPStatus, int] = HTTPStatus.OK,
        operation_id: str = None,
        description: str = "Successful Response"
    ):
        """Expect request with a GET method.

        :param url:
        :param status_code:
        :return:
        """
        open_api_status_code = str(int(status_code))
        self.paths[url]["get"] = {
            "responses": {open_api_status_code: {"description": description, "content": {"application/json": {}}}},
        }

        if operation_id:
            self.paths[url]["get"]["operationId"] = operation_id

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
                            body=json.dumps({"detail": json.loads(e.json())}),
                            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                        )
                        return json.loads(response.json())

                    # Do something before
                    body = func(**event.path.dict())
                else:
                    body = func()

                response = BaseOutput(body=json.dumps(body), status_code=status_code)
                return json.loads(response.json())

            return wrapper_decorator

        return create_response

    def post(
        self,
        url,
        *,
        status_code: Union[HTTPStatus, int] = HTTPStatus.CREATED,
        operation_id: str = None,
        description: str = "Successful Response"
    ):
        """Expect request with a POST method.

        :param url:
        :param status_code:
        :return:
        """
        open_api_status_code = str(int(status_code))
        self.paths[url]["post"] = {
            "responses": {open_api_status_code: {"description": description, "content": {"application/json": {}}}},
        }

        if operation_id:
            self.paths[url]["get"]["operationId"] = operation_id

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
                                return json.loads(response.json())

                    # Do something before
                    body = func(*func_args, **func_kwargs)
                else:
                    body = func()

                response = BaseOutput(body=json.dumps(body), status_code=status_code)
                return json.loads(response.json())

            return wrapper_decorator

        return create_response
