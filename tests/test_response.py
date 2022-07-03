from pydantic_lambda_handler.main import PydanticLambdaHander

app = PydanticLambdaHander(title="PydanticLambdaHander")


@app.get("/")
def hello_handler():
    return {"message": "Hello World"}


@app.post("/")
def create_handler():
    return {"message": "success"}


def test_get_response():
    """
    test that the message is returned in the body
    """
    response = hello_handler({}, None)
    assert response["statusCode"] == 200
    assert response["body"] == {"message": "Hello World"}


def test_post_response():
    """
    test that the message is returned in the body
    """
    response = create_handler({}, None)
    assert response["statusCode"] == 201
    assert response["body"] == {"message": "success"}
