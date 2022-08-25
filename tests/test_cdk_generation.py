from pydantic_lambda_handler.hooks.cdk_conf_hook import add_resource


def test_generate_cdk_config(cdk_config):
    hello_resource = next(i for i in cdk_config if i.get("name") == "hello")
    assert hello_resource["name"] == "hello", cdk_config["resources"]
    assert hello_resource["methods"] == [
        {
            "function_name": "HelloHandler",
            "handler": "hello_handler",
            "index": "demo_app_handlers.py",
            "method": "get",
            "reference": "demo_app_handlers.hello_handler",
            "status_code": "200",
        },
        {
            "function_name": "CreateHandler",
            "handler": "create_handler",
            "index": "demo_app_handlers.py",
            "method": "post",
            "reference": "demo_app_handlers.create_handler",
            "status_code": "201",
        },
    ]


def test_generate_cdk_config_status_code(cdk_config):
    hello_resource = next(i for i in cdk_config if i.get("name") == "hello")
    assert hello_resource["methods"][0]["status_code"] == "200"


def test_generate_cdk_config_nested_resources(cdk_config):
    hello_resource = next(i for i in cdk_config if i.get("name") == "items")
    assert hello_resource["resources"] == [
        {
            "methods": [
                {
                    "function_name": "HandlerWithTypeHint",
                    "handler": "handler_with_type_hint",
                    "index": "subfolder/path_parameters_handlers.py",
                    "method": "get",
                    "reference": "subfolder.path_parameters_handlers.handler_with_type_hint",
                    "status_code": "200",
                }
            ],
            "name": "{item_id}",
        }
    ]


def test_add_resource_query():
    child_list = []
    url = "query"
    add_resource(child_list, url)
    assert child_list == [{"name": "query"}]


def test_add_resource_deep():
    child_list = []
    url = "pets/{petId}"
    add_resource(child_list, url)
    assert child_list == [{"name": "pets", "resources": [{"name": "{petId}"}]}]
