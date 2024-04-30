from dataclasses import asdict, fields
from datetime import datetime

from multiply_backend_coding_task.models import Goal, GoalType, User
from multiply_backend_coding_task.exceptions import CustomException
from multiply_backend_coding_task.utilities import find_next_available_id


class GoalService:
    def __init__(self, goal_store):
        self.goal_store = goal_store

    def validate_goal_data(self, goal_data):
        formatted_goal_data = {}
        # specifying the second parameter returns the value of the key
        # if it exists or the default (None)
        goal_id = goal_data.pop("goal_id", None)
        if goal_id is not None and goal_id not in self.goal_store:
            raise CustomException(f"failure: goal with id {goal_id} not found", 409)
        if goal_id is not None and "user" in goal_data:
            raise CustomException("failure: cannot edit user data", 409)
        for key in goal_data:
            if key not in [field.name for field in fields(Goal)]:
                raise CustomException(status_code=400, message="Goal data is not valid")
            else:
                formatted_goal_data[key] = goal_data[key]
        if "goal_type" in formatted_goal_data and not GoalType.has_value(
            goal_data["goal_type"]
        ):
            raise CustomException(status_code=400, message="Goal data is not valid")
        if "target_date" in formatted_goal_data:
            try:
                datetime_object = datetime.strptime(
                    formatted_goal_data["target_date"], "%Y-%m-%d"
                )
                formatted_goal_data["target_date"] = datetime_object.date()
            except Exception:
                raise CustomException(
                    status_code=400, message="failure: date is not valid"
                )
        if "user" in formatted_goal_data:
            try:
                user = User(**formatted_goal_data["user"])
                formatted_goal_data["user"] = user
            except Exception:
                raise CustomException(
                    status_code=400, message="failure: user is not valid"
                )
        try:
            goal = Goal(**formatted_goal_data)
            return goal, goal_id
        except Exception:
            raise CustomException(status_code=400, message="Goal data is not valid")

    def create_goal(self, goal):
        try:
            next_available_id = find_next_available_id(self.goal_store)
            self.goal_store[next_available_id] = goal
            return {"status_code": 200, "data": next_available_id}
        except Exception:
            raise CustomException(
                status_code=500, message="failure: goal could not be created"
            )

    def update_goal(self, latest_goal_update, goal_id):
        try:
            existing_goal = asdict(self.goal_store[goal_id])
            for item in latest_goal_update:
                existing_goal[item] = latest_goal_update[item]
            self.goal_store[goal_id] = {**existing_goal}
            return {"status_code": 200, "data": goal_id}
        except Exception:
            raise CustomException(
                status_code=500,
                message=f"failure: goal with id {goal_id} could not be updated",
            )

    def process_goal(self, goal_data):
        goal, goal_id = self.validate_goal_data(goal_data)
        if goal_id is not None:
            response = self.update_goal(asdict(goal), goal_id)
        else:
            response = self.create_goal(goal)
        return response

    def get_goal(self, goal_id):
        if goal_id in self.goal_store:
            goal = asdict(self.goal_store[goal_id])
            return {"data": goal, "status_code": 200}
        else:
            raise CustomException(f"failure: no goal found with id {goal_id}", 400)
