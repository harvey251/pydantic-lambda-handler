import inspect
from pathlib import Path
from typing import Any

from awslambdaric.lambda_context import LambdaContext

from pydantic_lambda_handler.middleware import BaseHook


class CDKConf(BaseHook):
    """Gen cdk conf"""

    cdk_stuff: list[dict] = list()
    _dir_path: Path
    _ret_dict = dict
    _function_name = str
    _status_code = str
    _method = None
    _url = None

    @classmethod
    def method_init(cls, **kwargs):
        cls._url = url = kwargs["url"]
        cls._method = kwargs["method"]
        cls._function_name = kwargs["function_name"]
        cls._status_code = str(int(kwargs["status_code"]))
        cls._ret_dict = add_resource(cls.cdk_stuff, url.lstrip("/"))
        if not cls._ret_dict:
            raise ValueError

    @classmethod
    def pre_path(cls, **kwargs) -> None:
        func = kwargs["func"]

        ret_dict = cls._ret_dict
        function_name = cls._function_name
        add_methods(cls._method, func, ret_dict, function_name, cls._status_code, cls._dir_path, cls._url)

    @classmethod
    def pre_func(cls, event, context) -> tuple[dict, LambdaContext]:
        return event, context

    @classmethod
    def post_func(cls, body) -> Any:
        return body

    @classmethod
    def generate(cls):
        return {}


def add_resource(child_list: list[dict], url):
    part, found, remaining = url.partition("/")
    if part:
        if resource := next((r for i in child_list for r in i.get("resources", ()) if r.get("name") == part), None):
            if remaining:
                child_resource: list[dict] = []
                resource["resources"] = child_resource
                return add_resource(child_resource, remaining)
        else:
            child_dict = {"name": part}
            child_list.append(child_dict)
            if remaining:
                child_resource = []
                child_dict["resources"] = child_resource
                return add_resource(child_resource, remaining)

    return child_list


def get_part(cdk_conf, parts):
    next_cdk_conf = next((i for i in cdk_conf if i.get("name") == parts[0]), None)
    if len(parts) > 1:
        return get_part(next_cdk_conf, parts[1:])
    return next_cdk_conf


def add_methods(method, func, ret_dict, function_name, open_api_status_code, root_dir: Path, url):
    parts = url.lstrip("/").split("/")

    conf_part = get_part(ret_dict, parts[-1:])

    method_item = {
        "method": method,
        "index": str(Path(inspect.getfile(func)).relative_to(root_dir)),
        "handler": func.__name__,
        "reference": f"{func.__module__}.{func.__qualname__}",
        "status_code": open_api_status_code,
        "function_name": function_name or to_camel_case(func.__name__),
    }
    if "methods" in conf_part:
        conf_part["methods"].append(method_item)
    else:
        conf_part["methods"] = [method_item]


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text.capitalize()
    return "".join(i.capitalize() for i in s)
