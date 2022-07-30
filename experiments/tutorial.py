"""
https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html#services-apigateway-tutorial-prereqs
"""
import subprocess

import constructs
from aws_cdk.aws_iam import Effect, Policy, PolicyDocument, PolicyStatement, Role

# check aws
from aws_cdk.aws_lambda import Runtime

# from aws_cdk import (
#     aws_events as events,
#     aws_lambda as lambda_,
#     aws_events_targets as targets,
#     core
# )


subprocess.run(["aws", "--version"])

import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_s3 as s3
from aws_cdk import App, Stack
from constructs import Construct


class HelloCdkStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # dynamodb.Table(self, "My First Table")

        policy_statement_1 = iam.PolicyStatement(
            actions=[
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:UpdateItem",
            ],
            effect=Effect.ALLOW,
            resources=["*"],
        )

        policy_statement_2 = iam.PolicyStatement(
            actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
            effect=Effect.ALLOW,
            resources=["*"],
        )

        document = iam.PolicyDocument(statements=[policy_statement_1, policy_statement_2])

        policy = iam.Policy(
            self,
            "id_123",
            policy_name="lambda-apigateway-policy",
            document=document,
        )

        user = iam.User(self, "myuser")

        myrole = iam.Role(self, "id_1234", role_name="lambda-apigateway-role", assumed_by=user)

        aws_lambda.Function(
            self,
            "example_lambda",
            handler="LambdaFunctionOverHttps.handler",
            code=aws_lambda.Code.from_asset("/Users/markharvey/PycharmProjects/pydantic-lambda-handler/experiments"),
            runtime=Runtime.PYTHON_3_9,
        )


app = App()
print(HelloCdkStack(app, "HelloCdkStack"))
print(app.synth())
print(app.outdir)
print(app.region)

subprocess.run(
    [
        "aws",
        "lambda",
        "invoke",
        "--function-name",
        "example_lambda",
        "--payload",
        "file://input.txt",
        "outputfile.txt",
        "--cli-binary-format",
        "raw-in-base64-out",
    ]
)
