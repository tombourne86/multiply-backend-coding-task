from datetime import datetime

from _pytest.python_api import raises
from hamcrest import equal_to, assert_that

from multiply_backend_coding_task.exceptions import CustomException
from multiply_backend_coding_task.goal_service import GoalService
from multiply_backend_coding_task.models import Goal, GoalType, User

datestring = "2024-12-12"

test_user = {"first_name": "Jan", "email": "jan@multiply.ai", "user_id": "123"}

test_goal_id = "999"

test_goal_data = {
    "goal_type": "WEDDING",
    "target_amount": 100.00,
    "target_date": datestring,
}

test_date = datetime.strptime(datestring, "%Y-%m-%d").date()

test_goal = Goal(
    goal_type=GoalType.NEW_CAR, target_amount=500.00, target_date=test_date
)

test_goal_store = {}

test_goal_service = GoalService(test_goal_store)


def test_validate_new_valid_goal_data():
    actual_response = test_goal_service.validate_goal_data(test_goal_data)
    expected_response = (
        Goal(
            user=None, goal_type="WEDDING", target_amount=100.0, target_date=test_date
        ),
        None,
    )
    assert_that(actual_response, equal_to(expected_response))


def test_validate_updated_valid_goal_data_without_user():
    test_goal_store["1"] = test_goal
    actual_response = test_goal_service.validate_goal_data(
        {**test_goal_data, "goal_id": "1"}
    )
    expected_response = (
        Goal(
            user=None, goal_type="WEDDING", target_amount=100.0, target_date=test_date
        ),
        "1",
    )
    assert_that(actual_response, equal_to(expected_response))


def test_validate_valid_goal_data_with_user():
    actual_response = test_goal_service.validate_goal_data(
        {**test_goal_data, "user": test_user}
    )
    expected_response = (
        Goal(
            user=User(user_id="123", first_name="Jan", email="jan@multiply.ai"),
            goal_type="WEDDING",
            target_amount=100.0,
            target_date=test_date,
        ),
        None,
    )
    assert_that(actual_response, equal_to(expected_response))


def test_raise_exception_for_invalid_goal_id():
    with raises(CustomException) as exception_info:
        test_goal_service.validate_goal_data({**test_goal_data, "goal_id": "2"})
    assert_that(exception_info.value.status_code, equal_to(409))
    assert_that(
        exception_info.value.message,
        equal_to("failure: goal with id 2 not found"),
    )


def test_raise_exception_for_goal_id_and_user():
    test_goal_store["1"] = test_goal
    with raises(CustomException) as exception_info:
        test_goal_service.validate_goal_data(
            {**test_goal_data, "goal_id": "1", "user": test_user}
        )
    assert_that(exception_info.value.status_code, equal_to(409))
    assert_that(
        exception_info.value.message,
        equal_to("failure: cannot edit user data"),
    )


def test_raise_exception_for_malformed_date_string():
    with raises(CustomException) as exception_info:
        test_goal_service.validate_goal_data(
            {**test_goal_data, "target_date": "2024/12/12"}
        )
    assert_that(exception_info.value.status_code, equal_to(400))
    assert_that(
        exception_info.value.message,
        equal_to("failure: date is not valid"),
    )


def test_store_goal():
    test_goal_store.clear()
    response = test_goal_service.create_goal(test_goal)
    assert_that(response, equal_to({"status_code": 200, "data": "1"}))


def test_update_goal():
    test_goal_store["1"] = test_goal
    actual_response = test_goal_service.update_goal(test_goal_data, "1")
    expected_response = {"status_code": 200, "data": "1"}
    assert_that(actual_response, equal_to(expected_response))


def test_return_goal_when_valid_id_supplied():
    test_goal_store["1"] = test_goal
    actual_response = test_goal_service.get_goal("1")
    expected_response = {
        "data": {
            "user": None,
            "goal_type": GoalType.NEW_CAR,
            "target_amount": 500.0,
            "target_date": test_date,
        },
        "status_code": 200,
    }
    assert_that(actual_response, equal_to(expected_response))
