import json
import os
import re
from pathlib import Path

import pytest
import requests

from pydantic_lambda_handler.gen_open_api_inspect import gen_open_api_inspect


def pytest_addoption(parser):
    parser.addoption("--live", action="store_true", help="Also test against real AWS")


class Response:
    def __init__(self, response):
        self._response = response

    @property
    def status_code(self):
        return self._response["statusCode"]

    def json(self):
        return json.loads(self._response["body"])


class RequestClient:
    def __init__(self):
        path = Path(__file__).parents[1].joinpath("demo_app/demo_app")
        self._spec, self._cdk_stuff, self._test = gen_open_api_inspect(path)

    def get(self, url, *args, **kwargs):
        event = {}
        context = None

        for comp_url, info in self._test["paths"].items():
            try:
                match = re.fullmatch(comp_url, url)
            except Exception as e:
                print(e)
                # None breaking here
                continue

            if match:
                decorated_function_ = info["get"]["handler"]["decorated_function"]
                event["pathParameters"] = match.groupdict()
                break
        else:  # No break
            raise ValueError

        function_ = self._test["paths"][comp_url]["get"]["handler"]["function"]
        response = decorated_function_(function_)(event, context)
        return Response(response)

    def post(self, url, *args, **kwargs):
        event = {}
        context = None
        for comp_url, info in self._test["paths"].items():
            match = re.fullmatch(url, comp_url)
            if match:
                decorated_function_ = info["post"]["handler"]["decorated_function"]
                break
        else:
            raise ValueError
        function_ = self._test["paths"][comp_url]["post"]["handler"]["function"]
        response = decorated_function_(function_)(event, context)
        return Response(response)


@pytest.fixture(scope="function")
def base_url(requests_client_type):
    return os.environ["BASE_URL"] if requests_client_type == "real" else ""


@pytest.fixture(scope="function")
def requests_client(requests_client_type):
    return requests if requests_client_type == "real" else RequestClient()


def pytest_generate_tests(metafunc):
    if "requests_client_type" in metafunc.fixturenames:
        types = ["mock"]
        if metafunc.config.getoption("live"):
            types.append("real")
        metafunc.parametrize("requests_client_type", types)


@pytest.fixture
def _gen():
    path = Path(__file__).parents[1].joinpath("demo_app/demo_app")
    schema, cdk_stuff, _ = gen_open_api_inspect(path)
    return schema, cdk_stuff


@pytest.fixture
def schema(_gen):
    schema, *_ = _gen
    return schema


@pytest.fixture
def cdk_config(_gen):
    _, cdk_config = _gen
    return cdk_config
