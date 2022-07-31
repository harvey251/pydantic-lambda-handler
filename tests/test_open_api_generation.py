from pathlib import Path

import pytest

from pydantic_lambda_handler.gen_open_api_inspect import gen_open_api_inspect


@pytest.fixture
def schema():
    path = Path(__file__).parents[1].joinpath("demo_app")
    return gen_open_api_inspect(path)


def test_generate_open_api_version(schema):
    assert schema["openapi"] == "3.0.2"


def test_generate_open_api_info(schema):
    assert schema["info"] == {"title": "PydanticLambdaHandler", "version": "0.0.0"}


def test_generate_open_api_info_path_get(schema):
    item_path = schema["paths"]["/"]["get"]["responses"]["200"]["content"]
    assert item_path == {"application/json": {}}


def test_generate_open_api_info_path_post(schema):
    item_path = schema["paths"]["/"]["post"]["responses"]["201"]["content"]
    assert item_path == {"application/json": {}}


def test_generate_open_api_status_code_int(schema):
    """Can accept an in or an Enum status code"""
    assert "418" in schema["paths"]["/teapot/"]["get"]["responses"]


def test_generate_open_api_path(schema):
    assert "/pets/{petId}" in schema["paths"]
    assert schema["paths"]["/pets/{petId}"]["get"].get("parameters") == [
        {"name": "petId", "in": "path", "required": True, "schema": {"type": "string"}}
    ]


def test_generate_open_operation_id(schema):
    assert schema["paths"]["/pets/{petId}"]["get"].get("operationId") == "Create Pet"
