from _pytest.python_api import raises
from hamcrest import assert_that, equal_to

from multiply_backend_coding_task.exceptions import CustomException
from multiply_backend_coding_task.models import User
from multiply_backend_coding_task.user_service import UserService

valid_user_data = {"first_name": "User1", "email": "user1@multiply.ai"}

valid_user = User(**valid_user_data, **{"user_id": "2"})

duplicate_user_data = {"first_name": "Jan", "email": "jan@multiply.ai"}

user_data_with_malformed_email = {"first_name": "User1", "email": "user1@@multiply.ai"}

test_user_store = {"1": User(user_id="1", first_name="Jan", email="jan@multiply.ai")}

test_user_service = UserService(test_user_store)


def test_validate_a_new_user():
    actual_response = test_user_service.validate_user_data(valid_user_data)
    expected_response = User(user_id="2", first_name="User1", email="user1@multiply.ai")
    assert_that(actual_response, equal_to(expected_response))


def test_raise_exception_for_an_existing_user():
    with raises(CustomException) as exception_info:
        test_user_service.validate_user_data(duplicate_user_data)
    assert_that(exception_info.value.status_code, equal_to(409))
    assert_that(
        exception_info.value.message,
        equal_to("failure: jan@multiply.ai already exists"),
    )


def test_raise_exception_for_a_malformed_email():
    with raises(CustomException) as exception_info:
        test_user_service.validate_user_data(user_data_with_malformed_email)
    assert_that(exception_info.value.status_code, equal_to(400))
    assert_that(
        exception_info.value.message, equal_to("failure: invalid email address")
    )


def test_create_user():
    response = test_user_service.create_user(valid_user)
    assert_that(
        response,
        equal_to({"status_code": 200}),
    )
