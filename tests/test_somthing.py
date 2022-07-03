from src.pydantic_lambda_hander import PydanticLambdaHander

app = PydanticLambdaHander()


@app.get("/index")
def hello_handler():
    return {"message": "Hello World"}


def test_root():
    response = hello_handler({}, None)
    assert response["statusCode"] == 200
    assert response["body"] == {"message": "Hello World"}