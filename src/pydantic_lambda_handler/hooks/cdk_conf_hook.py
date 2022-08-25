import inspect
from collections import defaultdict
from operator import itemgetter
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

    _hold_dict = defaultdict(dict)

    @classmethod
    def method_init(cls, **kwargs):
        cls._url = url = kwargs["url"]
        cls._method = kwargs["method"].upper()
        cls._function_name = kwargs["function_name"]
        cls._status_code = str(int(kwargs["status_code"]))
        cls._ret_dict = add_resource(cls.cdk_stuff, url.lstrip("/"))
        cls._hold_dict[kwargs["url"]].update(
            {
                cls._method: {
                    "function_name": cls._function_name,
                    "status_code": cls._status_code,
                }
            }
        )
        if not cls._ret_dict:
            raise ValueError

    @classmethod
    def pre_path(cls, **kwargs) -> None:
        func = kwargs["func"]
        cls._hold_dict[kwargs["url"]][cls._method]["index"] = str(
            Path(inspect.getfile(func)).relative_to(cls._dir_path)
        )
        cls._hold_dict[kwargs["url"]][cls._method]["handler"] = func.__name__
        cls._hold_dict[kwargs["url"]][cls._method]["reference"] = f"{func.__module__}.{func.__qualname__}"
        cls._hold_dict[kwargs["url"]][cls._method]["function_name"] = cls._hold_dict[kwargs["url"]][cls._method][
            "function_name"
        ] or to_camel_case(func.__name__)

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

        methods = ("GET", "POST")

        resource = []
        for url, conf in sorted(cls._hold_dict.items()):
            add_resource_v2(resource, url.strip("/"), conf)

        def sort_recursive(resource_list: list[dict]):
            resource_list.sort(key=itemgetter("name"))
            seen = set()
            for i in resource_list:
                if "methods" in i:
                    i["methods"].sort(key=lambda x: methods.index(x["method"]))

                if i["name"] in seen:
                    raise ValueError(f'{i["name"]=}')

                seen.add(i["name"])

                if "resources" in i:
                    sort_recursive(i["resources"])

        sort_recursive(resource)
        return resource


def add_resource_v2(child_list: list[dict], url: str, conf):
    name, found, remaining = url.partition("/")
    # if not found:
    #     return child_list

    if not name and not found and not remaining:
        methods = {}
        child_list.append({"methods": methods, "name": name})
        for method, method_conf in conf.items():
            methods[method] = add_method_v2(method, method_conf)
    elif remaining:
        # need to keep traversing
        child_resource = next((i for i in child_list if i.get("name") == name), None)
        if not child_resource:
            child_resource = {}
            if name:
                child_resource["name"] = name
            resources = []
            child_resource["resources"] = resources
            child_list.append(child_resource)
            add_resource_v2(resources, remaining, conf)
        else:
            print()
    else:
        # add methods
        child_resource = next((i for i in child_list if i.get("name") == name), None)
        if not child_resource:
            # resources = []
            # child_resource["resources"] = resources
            child_resource = {"name": name}
            child_list.append({"resources": [child_resource]})

        if "methods" in child_resource:
            methods = child_resource["methods"]
        else:
            methods = {}
            child_resource["methods"] = methods

        for method, method_conf in conf.items():
            methods[method] = add_method_v2(method, method_conf)

        #
        # if "methods" in child_resource:
        #     methods = child_resource["methods"]
        # else:
        #     methods = {}
        #     child_resource["methods"] = methods
        #
        # for method, method_conf in conf.items():
        #     methods[method] = add_method_v2(method, method_conf)
    # else:
    #     child_resource = next((i for i in child_list if i.get("name") == name), None)
    #     if not child_resource:
    #         child_resource = {"name": name}
    #         child_list.append({"resources": [child_resource]})
    #
    #     if "methods" in child_resource:
    #         methods = child_resource["methods"]
    #     else:
    #         methods = {}
    #         child_resource["methods"] = methods
    #
    #     for method, method_conf in conf.items():
    #         methods[method] = add_method_v2(method, method_conf)
    #
    #     if "resources" in child_resource:
    #         resources = child_resource["resources"]
    #     else:
    #         resources = []
    #         child_resource["resources"] = resources
    #
    #     add_resource_v2(resources, remaining, conf)
    # if part:
    #     if resource := next((i for i in child_list if i.get("name") == part), None):
    #         if remaining:
    #             child_resource: list[dict] = []
    #             resource["resources"] = child_resource
    #             return add_resource(child_resource, remaining)
    #     else:
    #         child_dict = {"name": part}
    #         child_list.append(child_dict)
    #         if remaining:
    #             child_resource = []
    #             child_dict["resources"] = child_resource
    #             return add_resource(child_resource, remaining)
    # else:
    #     if next((i for i in child_list if i.get("name") == part), None) is None:
    #         child_dict = {"name": part}
    #         child_list.append(child_dict)

    return child_list


def add_resource(child_list: list[dict], url):
    part, found, remaining = url.partition("/")
    if part:
        if resource := next((i for i in child_list if i.get("name") == part), None):
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
    else:
        if next((i for i in child_list if i.get("name") == part), None) is None:
            child_dict = {"name": part}
            child_list.append(child_dict)

    return child_list


def get_part(cdk_conf, parts):
    try:
        next_cdk_conf = next((i for i in cdk_conf if i.get("name") == parts[0]))
    except StopIteration as e:
        print(cdk_conf, parts)
        print(e)
        raise

    if len(parts) > 1:
        return get_part(next_cdk_conf, parts[1:])
    return next_cdk_conf


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text.capitalize()
    return "".join(i.capitalize() for i in s)


def add_methods(method, func, ret_dict, function_name, open_api_status_code, root_dir: Path, url):
    parts = url.lstrip("/").split("/")

    method_item = {
        "method": method,
        "index": str(Path(inspect.getfile(func)).relative_to(CDKConf._dir_path)),
        "handler": func.__name__,
        "reference": f"{func.__module__}.{func.__qualname__}",
        "status_code": open_api_status_code,
        "function_name": function_name or to_camel_case(func.__name__),
    }

    conf_part = get_part(ret_dict, parts[-1:])
    if "methods" in conf_part:
        conf_part["methods"].append(method_item)
    else:
        conf_part["methods"] = [method_item]


def add_method_v2(method, conf):
    return {
        "method": method,
        "index": conf["index"],
        "handler": conf["handler"],
        "reference": conf["reference"],
        "status_code": conf["status_code"],
        "function_name": conf["function_name"],
    }
