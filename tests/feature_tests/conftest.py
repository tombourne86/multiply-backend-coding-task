from datetime import datetime

import pytest

from multiply_backend_coding_task.models import Goal, GoalType, User
from multiply_backend_coding_task.api import app, get_goal_store, get_user_store

datestring = "2024-12-12"

test_date = datetime.strptime(datestring, "%Y-%m-%d").date()

test_goal = Goal(
    goal_type=GoalType.NEW_CAR, target_amount=500.00, target_date=test_date
)

test_user = User(user_id="1", first_name="Jan", email="jan@multiply.ai")


@pytest.fixture(scope="session")
def test_client_with_no_data():
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    with app.test_request_context("/"):
        yield testing_client
    ctx.pop()


@pytest.fixture(scope="function")
def test_client_with_user_data():
    test_user_store = get_user_store()
    test_user_store["1"] = test_user
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    with app.test_request_context("/"):
        yield testing_client
    ctx.pop()
    test_user_store.clear()


@pytest.fixture(scope="function")
def test_client_with_goal_data():
    test_goal_store = get_goal_store()
    test_goal_store["1"] = test_goal
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    with app.test_request_context("/"):
        yield testing_client
    ctx.pop()
    test_goal_store.clear()
