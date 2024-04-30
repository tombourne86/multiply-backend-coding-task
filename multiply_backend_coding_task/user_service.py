from dataclasses import asdict

from multiply_backend_coding_task.exceptions import CustomException
from multiply_backend_coding_task.models import User
from multiply_backend_coding_task.utilities import (
    email_is_valid,
    find_next_available_id,
)


class UserService:
    def __init__(self, user_store):
        self.user_store = user_store

    def validate_user_data(self, user_data):
        if (
            (len(user_data) == 2)
            and ("first_name" in user_data)
            and ("email" in user_data)
        ):
            if email_is_valid(user_data["email"]):
                next_available_id = find_next_available_id(self.user_store)
                valid_user = User(**user_data, **{"user_id": next_available_id})
                if valid_user.email in [
                    asdict(user)["email"] for user in self.user_store.values()
                ]:
                    raise CustomException(
                        f"failure: {valid_user.email} already exists", 409
                    )
                else:
                    return valid_user
            else:
                raise CustomException("failure: invalid email address", 400)
        else:
            raise CustomException("failure: invalid user data", 400)

    def create_user(self, user):
        self.user_store[user.user_id] = user
        return {"status_code": 200}

    def register_user(self, user_data):
        user = self.validate_user_data(user_data)
        response = self.create_user(user)
        return response
