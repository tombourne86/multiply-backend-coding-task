def test_get_goal_with_valid_id(test_client_with_goal_data):
    response = test_client_with_goal_data.get("/goal", json={"goalId": "1"})
    assert response.json["status"] == 200
    assert response.json["data"] == {
        "goal_type": "NEW_CAR",
        "target_amount": 500.0,
        "target_date": "Thu, 12 Dec 2024 00:00:00 GMT",
        "user": None,
    }


def test_get_goal_with_invalid_id(test_client_with_goal_data):
    response = test_client_with_goal_data.get("/goal", json={"goalId": "1234567890"})
    assert response.status_code == 400
    assert response.text == "failure: no goal found with id 1234567890"


def test_create_goal_without_user(test_client_with_goal_data):
    response = test_client_with_goal_data.post(
        "/goal", json={"goalType": "WEDDING", "targetAmount": 100.00}
    )
    assert response.json["status"] == 200
    assert response.json["data"] == "2"


def test_create_goal_with_user(test_client_with_goal_data):
    response = test_client_with_goal_data.post(
        "/goal",
        json={
            "goalType": "WEDDING",
            "targetAmount": 100.00,
            "user": {"first_name": "Jan", "email": "jan@multiply.ai", "user_id": "123"},
        },
    )
    assert response.json["status"] == 200
    assert response.json["data"] == "2"


def test_create_goal_with_invalid_type(test_client_with_no_data):
    response = test_client_with_no_data.post(
        "/goal", json={"goalType": "SOMETHING_WRONG", "targetAmount": 100.00}
    )
    assert response.status_code == 400
    assert response.text == "Goal data is not valid"


def test_create_goal_with_invalid_date(test_client_with_no_data):
    response = test_client_with_no_data.post(
        "/goal", json={"targetDate": "2024/12/01", "targetAmount": 100.00}
    )
    assert response.status_code == 400
    assert response.text == "failure: date is not valid"


def test_create_goal_with_invalid_user(test_client_with_no_data):
    response = test_client_with_no_data.post(
        "/goal",
        json={
            "targetDate": "2024-12-01",
            "targetAmount": 100.00,
            "user": {"first_name": "User1", "email": "user1@multiply.ai"},
        },
    )
    assert response.status_code == 400
    assert response.text == "failure: user is not valid"
