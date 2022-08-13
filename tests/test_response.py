from demo_app import create_handler  # type: ignore


def test_get_response(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    response = requests_client.get(f"{base_url}/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_post_response(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    body = {"name": "Foo", "description": "An optional description", "price": 45.2, "tax": 3.5}
    response = requests_client.post(f"{base_url}/hello", json=body)
    assert response.status_code == 201, response.json()
    assert response.json() == body


def test_post_invalid_body(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    body = {
        "description": "An optional description",
        "price": 45.2,
    }
    response = requests_client.post(f"{base_url}/hello", json=body)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]
    }


def test_inv():
    event = {
        "resource": "/hello",
        "path": "/hello",
        "httpMethod": "POST",
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-ASN": "5378",
            "CloudFront-Viewer-Country": "GB",
            "Content-Type": "application/json",
            "Host": "eeepzcccn0.execute-api.eu-west-2.amazonaws.com",
            "User-Agent": "python-requests/2.28.1",
            "Via": "1.1 e46d5e94093ff4a4a8b6b4e0d2227692.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "xI6LbK4Pwj3p5Sr0aiGZpqcRepdUTI3YKd_thcra9QR-3a1AImOjgQ==",
            "X-Amzn-Trace-Id": "Root=1-62f7b424-015710506f08af806840c69f",
            "X-Forwarded-For": "90.252.101.71, 130.176.96.146",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "multiValueHeaders": {
            "Accept": ["*/*"],
            "Accept-Encoding": ["gzip, deflate"],
            "CloudFront-Forwarded-Proto": ["https"],
            "CloudFront-Is-Desktop-Viewer": ["true"],
            "CloudFront-Is-Mobile-Viewer": ["false"],
            "CloudFront-Is-SmartTV-Viewer": ["false"],
            "CloudFront-Is-Tablet-Viewer": ["false"],
            "CloudFront-Viewer-ASN": ["5378"],
            "CloudFront-Viewer-Country": ["GB"],
            "Content-Type": ["application/json"],
            "Host": ["eeepzcccn0.execute-api.eu-west-2.amazonaws.com"],
            "User-Agent": ["python-requests/2.28.1"],
            "Via": ["1.1 e46d5e94093ff4a4a8b6b4e0d2227692.cloudfront.net (CloudFront)"],
            "X-Amz-Cf-Id": ["xI6LbK4Pwj3p5Sr0aiGZpqcRepdUTI3YKd_thcra9QR-3a1AImOjgQ=="],
            "X-Amzn-Trace-Id": ["Root=1-62f7b424-015710506f08af806840c69f"],
            "X-Forwarded-For": ["90.252.101.71, 130.176.96.146"],
            "X-Forwarded-Port": ["443"],
            "X-Forwarded-Proto": ["https"],
        },
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "resourceId": "qdpoun",
            "resourcePath": "/hello",
            "httpMethod": "POST",
            "extendedRequestId": "WzkVyHJoLPEFWjw=",
            "requestTime": "13/Aug/2022:14:24:36 +0000",
            "path": "/prod/hello",
            "accountId": "691242900137",
            "protocol": "HTTP/1.1",
            "stage": "prod",
            "domainPrefix": "eeepzcccn0",
            "requestTimeEpoch": 1660400676838,
            "requestId": "86700358-cb7a-4521-bea9-d59b5b9f7d15",
            "identity": {
                "cognitoIdentityPoolId": None,
                "accountId": None,
                "cognitoIdentityId": None,
                "caller": None,
                "sourceIp": "90.252.101.71",
                "principalOrgId": None,
                "accessKey": None,
                "cognitoAuthenticationType": None,
                "cognitoAuthenticationProvider": None,
                "userArn": None,
                "userAgent": "python-requests/2.28.1",
                "user": None,
            },
            "domainName": "eeepzcccn0.execute-api.eu-west-2.amazonaws.com",
            "apiId": "eeepzcccn0",
        },
        "body": '{"name": "Foo", "description": "An optional description", "price": 45.2, "tax": 3.5}',
        "isBase64Encoded": False,
    }

    response = create_handler(event, {})

    assert response["statusCode"] == 201
