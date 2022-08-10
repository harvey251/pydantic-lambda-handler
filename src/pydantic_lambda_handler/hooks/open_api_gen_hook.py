import re
from inspect import signature
from typing import Any

from pydantic import create_model

from pydantic_lambda_handler.main import PydanticLambdaHandler
from pydantic_lambda_handler.middleware import BaseHook


class APIGenerationHook(BaseHook):
    """Gen open api"""

    title: str
    version: str
    paths: dict[str, Any] = {}

    @classmethod
    def method_init(cls, **kwargs):
        app: PydanticLambdaHandler = kwargs["self"]
        status_code = kwargs["status_code"]
        open_api_status_code = str(int(status_code))
        method = kwargs["method"]
        APIGenerationHook.title = app.title
        APIGenerationHook.version = app.version

        url = kwargs["url"]
        if url in cls.paths:
            cls.paths[url].update(
                {
                    method: {
                        "responses": {
                            open_api_status_code: {
                                "description": kwargs["description"],
                                "content": {"application/json": {}},
                            }
                        },
                    }
                }
            )
        else:
            cls.paths[url] = {
                method: {
                    "responses": {
                        open_api_status_code: {
                            "description": kwargs["description"],
                            "content": {"application/json": {}},
                        }
                    },
                }
            }

        if kwargs["operation_id"]:
            cls.paths[url][method]["operationId"] = kwargs["operation_id"]

    @classmethod
    def pre_path(cls, **kwargs) -> None:
        sig = signature(kwargs["func"])

        if sig.parameters:

            url = kwargs["url"]
            method = kwargs["method"]

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

            cls.paths[url][method]["parameters"] = properties

    @classmethod
    def pre_func(cls, event, context) -> tuple[dict, Any]:
        return event, context

    @classmethod
    def post_func(cls, body) -> Any:
        return body

    @classmethod
    def generate(cls):
        return {
            "openapi": "3.0.2",
            "info": {"title": cls.title, "version": cls.version},
            "paths": cls.paths,
        }
