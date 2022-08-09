def test_generate_cdk_config(cdk_config):
    assert cdk_config["resources"]["hello"]["methods"] == {
        "get": {"function_name": "helloHandler", "reference": "demo_app.hello_handler", "status_code": "200"},
        "post": {"function_name": "createHandler", "reference": "demo_app.create_handler", "status_code": "201"},
    }


def test_generate_cdk_config_status_code(cdk_config):
    assert cdk_config["resources"]["hello"]["methods"]["get"]["status_code"] == "200"


def test_generate_cdk_config_nested_resources(cdk_config):
    assert cdk_config["resources"]["items"] == {
        "resources": {
            "{item_id}": {
                "methods": {
                    "get": {
                        "function_name": "handlerWithTypeHint",
                        "reference": "subfolder.path_parameters.handler_with_type_hint",
                        "status_code": "200",
                    }
                }
            }
        }
    }
