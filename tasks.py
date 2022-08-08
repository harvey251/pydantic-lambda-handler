import json
import subprocess
from pathlib import Path

import requests
from invoke import task

from pydantic_lambda_handler.gen_open_api_inspect import gen_open_api_inspect


@task
def build_and_deploy(c):
    root = Path(__name__).parent
    demo_app_dir = root.joinpath("demo_app")

    subprocess.run(f"cdk bootstrap", check=True, shell=True, cwd=demo_app_dir)
    subprocess.run("cdk deploy --require-approval never", check=True, shell=True, cwd=demo_app_dir)

    run_live_tests(c)


@task
def run_live_tests(c):
    response = requests.get(
        "https://eeepzcccn0.execute-api.eu-west-2.amazonaws.com/prod/hello",
        headers={"x-api-key": "mgq5m45xZt53z7wHwikLj9zDiJo7Ovio2C2ZY7AU"},
    )
    response.raise_for_status()

    response = requests.post(
        "https://eeepzcccn0.execute-api.eu-west-2.amazonaws.com/prod/hello",
        headers={"x-api-key": "mgq5m45xZt53z7wHwikLj9zDiJo7Ovio2C2ZY7AU"},
        json={},
    )
    response.raise_for_status()


@task
def generate_open_api_spec(c):
    path = Path(__file__).parent.joinpath("demo_app/demo_app")
    schema, *_ = gen_open_api_inspect(path)
    with path.joinpath("open_api_spec.json").open("w") as f:
        json.dump(schema, f, indent=4)
