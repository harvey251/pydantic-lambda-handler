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


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text.capitalize()
    return "".join(i.capitalize() for i in s)


class PydanticLambdaHandler:
    """
    The decorator handle.
    """

    paths: dict = defaultdict(dict)
    cdk_stuff: dict = defaultdict(dict)
    testing_stuff: dict = defaultdict(dict)

    def __init__(self, *, title="PydanticLambdaHandler", version="0.0.0"):
        self.title = title
        self.version = version

    @classmethod
    def get(
        cls,
        url,
        *,
        status_code: Union[HTTPStatus, int] = HTTPStatus.OK,
        operation_id: str = None,
        description: str = "Successful Response",
        function_name=None,
    ):
        """Expect request with a GET method.

        :param url:
        :param status_code:
        :return:
        """
        open_api_status_code = str(int(status_code))
        cls.paths[url]["get"] = {
            "responses": {open_api_status_code: {"description": description, "content": {"application/json": {}}}},
        }

        def add_resource(child_dict: dict, url):
            part, found, remaining = url.partition("/")
            if part:
                if part in child_dict.get("resources", {}):
                    return add_resource(child_dict["resources"][part], remaining)

                last_resource: dict[str, dict] = {}
                if "resources" not in child_dict:
                    child_dict["resources"] = {part: last_resource}
                else:
                    child_dict["resources"].update({part: last_resource})

                return add_resource(child_dict["resources"][part], remaining)
            return child_dict

        ret_dict = add_resource(cls.cdk_stuff, url.lstrip("/"))

        testing_url = url.replace("{", "(?P<").replace("}", r">\w+)")
        if testing_url not in cls.testing_stuff["paths"]:
            cls.testing_stuff["paths"][testing_url] = {"get": {}}
        else:
            cls.testing_stuff["paths"][testing_url]["get"] = {}

        if operation_id:
            cls.paths[url]["get"]["operationId"] = operation_id

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
                # f"{func.__module__}.{func.__qualname__}"
                cls.paths[url]["get"]["parameters"] = properties

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

            if "methods" in ret_dict:
                ret_dict["methods"]["get"] = {
                    "reference": f"{func.__module__}.{func.__qualname__}",
                    "status_code": open_api_status_code,
                    "function_name": function_name or to_camel_case(func.__name__),
                }
            else:
                ret_dict["methods"] = {
                    "get": {
                        "reference": f"{func.__module__}.{func.__qualname__}",
                        "status_code": open_api_status_code,
                        "function_name": function_name or to_camel_case(func.__name__),
                    }
                }

            cls.testing_stuff["paths"][testing_url]["get"]["handler"]["function"] = func

            return wrapper_decorator

        cls.testing_stuff["paths"][testing_url]["get"]["handler"] = {"decorated_function": create_response}
        return create_response

    @classmethod
    def post(
        cls,
        url,
        *,
        status_code: Union[HTTPStatus, int] = HTTPStatus.CREATED,
        operation_id: str = None,
        description: str = "Successful Response",
        function_name=None,
    ):
        """Expect request with a POST method.

        :param url:
        :param status_code:
        :return:
        """
        open_api_status_code = str(int(status_code))
        cls.paths[url]["post"] = {
            "responses": {open_api_status_code: {"description": description, "content": {"application/json": {}}}},
        }

        if operation_id:
            cls.paths[url]["post"]["operationId"] = operation_id

        def add_resource(child_dict: dict, url):
            part, found, remaining = url.partition("/")
            if part:
                if part in child_dict.get("resources", {}):
                    return add_resource(child_dict["resources"][part], remaining)

                last_resource: dict[str, dict] = {}
                if "resources" not in child_dict:
                    child_dict["resources"] = {part: last_resource}
                else:
                    child_dict["resources"].update({part: last_resource})

                return add_resource(child_dict["resources"][part], remaining)
            return child_dict

        ret_dict = add_resource(cls.cdk_stuff, url.lstrip("/"))

        testing_url = url.replace("{", "(?P<").replace("}", r">\w+)")
        if testing_url not in cls.testing_stuff["paths"]:
            cls.testing_stuff["paths"][testing_url] = {"post": {}}
        else:
            cls.testing_stuff["paths"][testing_url]["post"] = {}

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

            if "methods" in ret_dict:
                ret_dict["methods"]["post"] = {
                    "reference": f"{func.__module__}.{func.__qualname__}",
                    "status_code": open_api_status_code,
                    "function_name": function_name or to_camel_case(func.__name__),
                }
            else:
                ret_dict["methods"] = {
                    "post": {
                        "reference": f"{func.__module__}.{func.__qualname__}",
                        "status_code": open_api_status_code,
                        "function_name": function_name or to_camel_case(func.__name__),
                    }
                }

            cls.testing_stuff["paths"][testing_url]["post"]["handler"]["function"] = func

            return wrapper_decorator

        cls.testing_stuff["paths"][testing_url]["post"]["handler"] = {"decorated_function": create_response}
        return create_response
