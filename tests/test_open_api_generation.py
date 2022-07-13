from pathlib import Path

from pydantic_lambda_handler.gen_open_api_inspect import gen_open_api_inspect


def test_generate_open_api_version():
    path = Path(__file__).parent.joinpath("demo")
    schema = gen_open_api_inspect(path)

    assert schema["openapi"] == "3.0.2"


def test_generate_open_api_info():
    path = Path(__file__).parent.joinpath("demo")
    schema = gen_open_api_inspect(path)

    assert schema["info"] == {"title": "PydanticLambdaHandler"}


def test_generate_open_api_info_path_get():
    path = Path(__file__).parent.joinpath("demo")
    schema = gen_open_api_inspect(path)

    item_path = schema["paths"]["/"]["get"]["responses"]["200"]["content"]
    assert item_path == {"application/json": {}}


def test_generate_open_api_info_path_post():
    path = Path(__file__).parent.joinpath("demo")
    schema = gen_open_api_inspect(path)

    item_path = schema["paths"]["/"]["post"]["responses"]["201"]["content"]
    assert item_path == {"application/json": {}}


def test_generate_open_api_status_code_int():
    """Can accept an in or an Enum status code"""
    path = Path(__file__).parent.joinpath("demo")
    schema = gen_open_api_inspect(path)

    assert "418" in schema["paths"]["/teapot/"]["get"]["responses"]


def test_generate_open_api_path():
    path = Path(__file__).parent.joinpath("demo")
    schema = gen_open_api_inspect(path)

    assert "/pets/{petId}" in schema["paths"]
    assert schema["paths"]["/pets/{petId}"]["get"].get("parameters") == [
        {"name": "petId", "in": "path", "required": True, "schema": {"type": "string"}}
    ]


def test_generate_open_operation_id():
    path = Path(__file__).parent.joinpath("demo")
    schema = gen_open_api_inspect(path)

    assert schema["paths"]["/pets/{petId}"]["get"].get("operationId") == "Create Pet"
