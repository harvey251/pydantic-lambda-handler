"""
https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html#services-apigateway-tutorial-prereqs
"""
from aws_cdk import BundlingOptions, Stack
from aws_cdk import aws_apigateway as _apigw
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda
from constructs import Construct


class DemoAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        policy_statement_1 = iam.PolicyStatement(
            actions=[
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:UpdateItem",
            ],
            effect=iam.Effect.ALLOW,
            resources=["*"],
        )

        policy_statement_2 = iam.PolicyStatement(
            actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
            effect=iam.Effect.ALLOW,
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

        base_lambda_layer = aws_lambda.LayerVersion(
            self,
            "base_layer",
            code=aws_lambda.Code.from_asset(
                "/Users/markharvey/PycharmProjects/pydantic-lambda-handler/demo_app_requirements",
            ),
        )

        base_lambda = aws_lambda.Function(
            self,
            "function",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="subfolder.a_file.index_handler",
            layers=[base_lambda_layer],
            code=aws_lambda.Code.from_asset(
                "/Users/markharvey/PycharmProjects/pydantic-lambda-handler/demo_app/demo_app",
            ),
        )

        base_api = _apigw.RestApi(self, "ApiGatewayWithCors", rest_api_name="ApiGatewayWithCors")

        example_entity = base_api.root.add_resource(
            "index",
            default_cors_preflight_options=_apigw.CorsOptions(
                allow_methods=["GET", "OPTIONS"], allow_origins=_apigw.Cors.ALL_ORIGINS
            ),
        )

        example_entity_lambda_integration = _apigw.LambdaIntegration(
            base_lambda,
            proxy=True,
            integration_responses=[
                _apigw.IntegrationResponse(
                    status_code="200", response_parameters={"method.response.header.Access-Control-Allow-Origin": "'*'"}
                )
            ],
        )

        example_entity.add_method(
            "GET",
            example_entity_lambda_integration,
            method_responses=[
                _apigw.MethodResponse(
                    status_code="200", response_parameters={"method.response.header.Access-Control-Allow-Origin": True}
                )
            ],
        )

        # need to set endpoint type to regional

        # needs to be a Proxy Intergration

        # API gateway  -> Model schema needs to be declared
        # API gateway  -> Documentation schema needs to be declared
