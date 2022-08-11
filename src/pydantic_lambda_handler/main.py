"""
The main class which you import and use a decorator.
"""
import functools
import json
import re
from collections import defaultdict
from http import HTTPStatus
from inspect import signature
from typing import Iterable, Optional, Union

from orjson import loads
from pydantic import ValidationError, create_model

from pydantic_lambda_handler.middleware import BaseHook
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

    cdk_stuff: dict = defaultdict(dict)
    testing_stuff: dict = defaultdict(dict)
    _hooks: list[type[BaseHook]] = []

    def __init__(
        self, *, title="PydanticLambdaHandler", version="0.0.0", hooks: Optional[Iterable[type[BaseHook]]] = None
    ):
        self.title = title
        self.version = version
        if hooks:
            PydanticLambdaHandler._hooks.extend(hooks)

    @classmethod
    def add_hook(cls, hook: type[BaseHook]):
        cls._hooks.append(hook)

    def get(
        self,
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
        method = "get"
        for hook in self._hooks:
            hook.method_init(**locals())

        ret_dict = add_resource(self.cdk_stuff, url.lstrip("/"))

        testing_url = url.replace("{", "(?P<").replace("}", r">\w+)")
        if testing_url not in self.testing_stuff["paths"]:
            self.testing_stuff["paths"][testing_url] = {method: {}}
        else:
            self.testing_stuff["paths"][testing_url][method] = {}

        def create_response(func):
            for hook in self._hooks:
                hook.pre_path(**locals())

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

                EventModel = create_model("EventModel", path=(PathModel, {}))

            @functools.wraps(func)
            def wrapper_decorator(event, context):
                print(event)
                for hook in self._hooks:
                    event, context = hook.pre_func(event, context)
                if sig.parameters:
                    path_parameters = event.get("pathParameters", {}) or {}

                    try:
                        event = EventModel(path=path_parameters)
                    except ValidationError as e:
                        response = BaseOutput(
                            body=json.dumps({"detail": json.loads(e.json())}),
                            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                        )
                        return loads(response.json())

                    # Do something before
                    body = func(**event.path.dict())
                else:
                    body = func()

                for hook in reversed(self._hooks):
                    body = hook.post_func(body)

                response = BaseOutput(body=json.dumps(body), status_code=status_code)
                return loads(response.json())

            add_methods(method, func, ret_dict, function_name, str(int(status_code)))

            self.testing_stuff["paths"][testing_url][method]["handler"]["function"] = func

            return wrapper_decorator

        self.testing_stuff["paths"][testing_url][method]["handler"] = {"decorated_function": create_response}
        return create_response

    def post(
        self,
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
        method = "post"
        for hook in self._hooks:
            hook.method_init(**locals())

        ret_dict = add_resource(self.cdk_stuff, url.lstrip("/"))

        testing_url = url.replace("{", "(?P<").replace("}", r">\w+)")
        if testing_url not in self.testing_stuff["paths"]:
            self.testing_stuff["paths"][testing_url] = {method: {}}
        else:
            self.testing_stuff["paths"][testing_url][method] = {}

        def create_response(func):
            for hook in self._hooks:
                hook.pre_path(**locals())

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

                EventModel = create_model("EventModel", path=(PathModel, {}))

            @functools.wraps(func)
            def wrapper_decorator(event, context):
                for hook in self._hooks:
                    event, context = hook.pre_func(event, context)

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
                                return loads(response.json())

                    # Do something before

                    body = func(*func_args, **func_kwargs)
                else:
                    body = func()

                for hook in reversed(self._hooks):
                    body = hook.post_func(body)

                response = BaseOutput(body=json.dumps(body), status_code=status_code)
                return loads(response.json())

            add_methods(method, func, ret_dict, function_name, str(int(status_code)))

            self.testing_stuff["paths"][testing_url][method]["handler"]["function"] = func

            return wrapper_decorator

        self.testing_stuff["paths"][testing_url][method]["handler"] = {"decorated_function": create_response}
        return create_response


def add_methods(method, func, ret_dict, function_name, open_api_status_code):
    if "methods" in ret_dict:
        ret_dict["methods"][method] = {
            "reference": f"{func.__module__}.{func.__qualname__}",
            "status_code": open_api_status_code,
            "function_name": function_name or to_camel_case(func.__name__),
        }
    else:
        ret_dict["methods"] = {
            method: {
                "reference": f"{func.__module__}.{func.__qualname__}",
                "status_code": open_api_status_code,
                "function_name": function_name or to_camel_case(func.__name__),
            }
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
