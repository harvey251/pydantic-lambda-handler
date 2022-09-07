"""
location of base models
"""
from enum import Enum
from http import HTTPStatus
from typing import Union, Any, Optional, Dict

from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo, Undefined


class BaseOutput(BaseModel):
    """
    https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format

    {
        "isBase64Encoded": true | false,
        "statusCode": httpStatusCode,
        "headers": {"headerName": "headerValue", ...},
        "multiValueHeaders": {
            "headerName": ["headerValue", "headerValue2", ...],
            ...
        },
        "body": "..."
    }
    """

    isBase64Encoded: bool = Field(False, alias="is_base_64_encoded")
    statusCode: Union[HTTPStatus, int] = Field(..., alias="status_code")
    headers: dict[str, str] = Field(default_factory=dict, description='{"headerName": "headerValue", ...}')
    multiValueHeaders: dict[str, Union[str, list[str]]] = Field(
        default_factory=dict,
        description='{"headerName": ["headerValue", "headerValue2", ...], ...}',
        alias="multi_value_headers",
    )
    body: Union[dict, list, str, int]


class ParamTypes(Enum):
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"


class Param(FieldInfo):
    in_: ParamTypes

    def __init__(
        self,
        default: Any = Undefined,
        *,
        alias: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        lt: Optional[float] = None,
        le: Optional[float] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        regex: Optional[str] = None,
        example: Any = Undefined,
        examples: Optional[Dict[str, Any]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
        **extra: Any,
    ):
        self.deprecated = deprecated
        self.example = example
        self.examples = examples
        self.include_in_schema = include_in_schema
        super().__init__(
            default=default,
            alias=alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            **extra,
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"


class Path(Param):
    in_ = ParamTypes.path

    def __init__(
        self,
        default: Any = Undefined,
        *,
        alias: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        lt: Optional[float] = None,
        le: Optional[float] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        regex: Optional[str] = None,
        example: Any = Undefined,
        examples: Optional[dict[str, Any]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
        **extra: Any,
    ):
        self.in_ = self.in_
        super().__init__(
            default=...,
            alias=alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            deprecated=deprecated,
            example=example,
            examples=examples,
            include_in_schema=include_in_schema,
            **extra,
        )
