from pydantic_lambda_handler.main import PydanticLambdaHander

app = PydanticLambdaHander()


@app.get("/")
def hello_handler():
    return {"message": "Hello World"}


def test_response():
    """
    test that the message is returned in the body
    """
    response = hello_handler({}, None)
    assert response["statusCode"] == 200
    assert response["body"] == {"message": "Hello World"}
