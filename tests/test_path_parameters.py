from enum import Enum

import pytest

from pydantic_lambda_handler.main import PydanticLambdaHander

app = PydanticLambdaHander(title="PydanticLambdaHander")


@app.get("/items/{item_id}")
def handler(item_id):
    return {"item_id": item_id}


def test_path_parameters_without_typehint():
    event = {"pathParameters": {"item_id": "1"}}
    response = handler(event, None)
    assert response["statusCode"] == 200
    assert response["body"] == {"item_id": "1"}


@app.get("/items/{item_id}")
def handler_with_type_hint(item_id: int):
    return {"item_id": item_id}


def test_path_parameters_with_typehint():
    event = {"pathParameters": {"item_id": "1"}}
    response = handler_with_type_hint(event, None)
    assert response["statusCode"] == 200
    assert response["body"] == {"item_id": 1}


class Animals(str, Enum):
    dog = "dog"


@app.get("/items/{item_id}")
def handler_with_enum_type_hint(item_id: Animals):
    return {"item_id": item_id}


def test_path_parameters_with_enum_typehint():
    event = {"pathParameters": {"item_id": "dog"}}
    response = handler_with_enum_type_hint(event, None)
    assert response["statusCode"] == 200
    assert response["body"] == {"item_id": "dog"}


def test_path_parameters_with_typehint_typeerror():
    event = {"pathParameters": {"item_id": "cat"}}
    response = handler_with_type_hint(event, None)
    assert response["statusCode"] == 422
    assert response["body"] == {
        "detail": [
            {
                "loc": ["path", "item_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


def test_path_parameters_with_path_default():
    @app.get("/items/{item_id}")
    def handler_with_path_default(item_id=2):
        return {"item_id": item_id}

    with pytest.raises(Exception):
        handler_with_path_default({}, None)
