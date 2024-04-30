def test_hello_world_api(test_client_with_no_data):
    response = test_client_with_no_data.get("/")
    assert response.status_code == 200
    assert response.text == "Hello, world!"
