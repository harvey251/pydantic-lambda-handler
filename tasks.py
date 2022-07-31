import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from shutil import copy2
from tempfile import SpooledTemporaryFile, TemporaryDirectory, mkdtemp

import requests
from invoke import task

# from aws_cdk.aws_iam import Policy, PolicyDocument, PolicyStatement, Effect
from pydantic_lambda_handler.gen_open_api_inspect import gen_open_api_inspect


@task
def build_and_deploy(c):
    root = Path(__name__).parent
    # src = root.joinpath("src/pydantic_lambda_handler")
    requirements_dir = root.joinpath("demo_app_requirements")
    requirements_dir.mkdir(parents=True, exist_ok=True)
    demo_app_dir = root.joinpath("demo_app")
    shutil.rmtree(requirements_dir)
    # shutil.copytree(src, requirements_dir, symlinks=False, ignore=None, copy_function=copy2, ignore_dangling_symlinks=False,
    #                 dirs_exist_ok=True)

    # https://aws.amazon.com/premiumsupport/knowledge-center/lambda-python-package-compatible/
    # pip install \
    #     --platform manylinux2014_x86_64 \
    #     --target=my-lambda-function \
    #     --implementation cp \
    #     --python 3.9 \
    #     --only-binary=:all: --upgrade \
    #     pandas
    subprocess.run(
        (
            f"{sys.executable}",
            "-m",
            "pip",
            "install",
            ".",
            "--upgrade",
            "--target",
            requirements_dir.joinpath("python"),
            "--platform",
            "manylinux2014_x86_64",
            "--implementation",
            "cp",
            "--python",
            "3.9",
            "--only-binary=:all:",
        ),
        check=True,
    )

    subprocess.run("cdk bootstrap", check=True, shell=True, cwd=demo_app_dir)

    subprocess.run("cdk deploy", check=True, shell=True, cwd=demo_app_dir)

    response = requests.get(
        "https://eeepzcccn0.execute-api.eu-west-2.amazonaws.com/prod/index/",
        headers={"x-api-key": "mgq5m45xZt53z7wHwikLj9zDiJo7Ovio2C2ZY7AU"},
    )
    response.raise_for_status()


@task
def run_live_tests(c):
    response = requests.get(
        "https://eeepzcccn0.execute-api.eu-west-2.amazonaws.com/prod/index",
        headers={"x-api-key": "mgq5m45xZt53z7wHwikLj9zDiJo7Ovio2C2ZY7AU"},
    )
    response.raise_for_status()


@task
def generate_open_api_spec(c):
    path = Path(__file__).parent.joinpath("tests/demo")
    schema = gen_open_api_inspect(path)
    with path.joinpath("open_api_spec.json").open("w") as f:
        json.dump(schema, f, indent=4)
