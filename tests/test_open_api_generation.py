from pydantic_lambda_handler.main import PydanticLambdaHander


def test_generate_open_api():
    expected_api_schema = {
        "openapi": "3.0.2",
        "info": {"title": "PydanticLambdaHander", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
                    "responses": {"200": {"description": "Successful Response", "content": {"application/json": {}}}}
                }
            }
        },
    }

    app = PydanticLambdaHander(title="PydanticLambdaHander", version="0.1.0")

    @app.get("/items/")
    def hello_handler():
        return {"message": "Hello World"}

    schema = app.generate_open_api()
    assert schema == expected_api_schema


def test_generate_open_api_status_code_int():
    expected_api_schema = {
        "openapi": "3.0.2",
        "info": {"title": "PydanticLambdaHander", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
                    "responses": {"200": {"description": "Successful Response", "content": {"application/json": {}}}}
                }
            }
        },
    }

    app = PydanticLambdaHander(title="PydanticLambdaHander", version="0.1.0")

    @app.get("/items/", status_code=200)
    def hello_handler():
        return {"message": "Hello World"}

    schema = app.generate_open_api()
    assert schema == expected_api_schema
