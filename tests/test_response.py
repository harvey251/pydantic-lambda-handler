import json

from demo_app import create_handler, hello_handler  # type: ignore


def test_get_response():
    """
    test that the message is returned in the body
    """
    response = hello_handler({}, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"message": "Hello World"}


def test_post_response():
    """
    test that the message is returned in the body
    """
    response = create_handler({}, None)
    assert response["statusCode"] == 201
    assert json.loads(response["body"]) == {"message": "success"}
