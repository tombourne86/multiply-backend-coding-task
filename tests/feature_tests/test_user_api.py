def test_create_valid_user(test_client_with_no_data):
    response = test_client_with_no_data.post(
        "/user", json={"firstName": "Jan", "email": "jan@multiply.ai"}
    )
    assert response.status_code == 200


def test_create_duplicate_user(test_client_with_user_data):
    second_response = test_client_with_user_data.post(
        "/user", json={"firstName": "Jan", "email": "jan@multiply.ai"}
    )
    assert second_response.status_code == 409
    assert second_response.text == "failure: jan@multiply.ai already exists"


def test_create_invalid_user(test_client_with_no_data):
    response = test_client_with_no_data.post(
        "/user", json={"name": "Jan", "email": "jan@multiply.ai"}
    )
    assert response.status_code == 400
    assert response.text == "failure: invalid user data"
