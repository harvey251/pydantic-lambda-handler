def test_get_response(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    # requests_client.get("/hello")
    response = requests_client.get(f"{base_url}/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_post_response(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    response = requests_client.post(f"{base_url}/hello")
    assert response.status_code == 201
    assert response.json() == {"message": "success"}
