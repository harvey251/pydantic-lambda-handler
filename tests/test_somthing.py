import pytest

from pydantic_lambda_hander import PydanticLambdaHander

app = PydanticLambdaHander()


def root():
    return {"message": "Hello World"}


@pytest.mark.xfail()
def test_root():
    response = root()
    assert response == """body"""
