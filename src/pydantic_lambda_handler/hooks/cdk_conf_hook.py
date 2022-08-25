from collections import defaultdict
from typing import Any

from awslambdaric.lambda_context import LambdaContext

from pydantic_lambda_handler.middleware import BaseHook


class CDKConf(BaseHook):
    """Gen cdk conf"""

    cdk_stuff: dict = defaultdict(dict)
    _ret_dict = dict
    _function_name = str
    _status_code = str
    _method = None

    @classmethod
    def method_init(cls, **kwargs):
        url = kwargs["url"]
        cls._method = kwargs["method"]
        cls._function_name = kwargs["function_name"]
        cls._status_code = str(int(kwargs["status_code"]))
        cls._ret_dict = add_resource(cls.cdk_stuff, url.lstrip("/"))

    @classmethod
    def pre_path(cls, **kwargs) -> None:
        func = kwargs["func"]

        ret_dict = cls._ret_dict
        function_name = cls._function_name
        add_methods(cls._method, func, ret_dict, function_name, cls._status_code)

    @classmethod
    def pre_func(cls, event, context) -> tuple[dict, LambdaContext]:
        return event, context

    @classmethod
    def post_func(cls, body) -> Any:
        return body

    @classmethod
    def generate(cls):
        return {}


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


def add_methods(method, func, ret_dict, function_name, open_api_status_code):
    if "methods" in ret_dict:
        ret_dict["methods"][method] = {
            "reference": f"{func.__module__}.{func.__qualname__}".removeprefix("src.").removeprefix("demo_app."),
            "status_code": open_api_status_code,
            "function_name": function_name or to_camel_case(func.__name__),
        }
    else:
        ret_dict["methods"] = {
            method: {
                "reference": f"{func.__module__}.{func.__qualname__}".removeprefix("src.").removeprefix("demo_app."),
                "status_code": open_api_status_code,
                "function_name": function_name or to_camel_case(func.__name__),
            }
        }


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text.capitalize()
    return "".join(i.capitalize() for i in s)
