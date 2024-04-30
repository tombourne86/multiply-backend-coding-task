from flask import Flask, request, Response, jsonify

from multiply_backend_coding_task.exceptions import CustomException
from multiply_backend_coding_task.goal_service import GoalService
from multiply_backend_coding_task.user_service import UserService
from multiply_backend_coding_task.utilities import format_snake_case

app = Flask(__name__)

USER_STORE = {}
GOAL_STORE = {}


def get_user_store():
    return USER_STORE


def get_goal_store():
    return GOAL_STORE


user_service = UserService(get_user_store())
goal_service = GoalService(get_goal_store())


@app.route("/")
def hello_world():
    return "Hello, world!"


@app.route("/user", methods=["POST"])
def user():
    data = request.get_json()
    formatted_data = format_snake_case(data)
    response = user_service.register_user(formatted_data)
    return Response(status=response["status_code"])


@app.route("/goal", methods=["GET", "POST"])
def goal():
    data = request.get_json()
    if request.method == "GET":
        response = goal_service.get_goal(data["goalId"])
        return jsonify(data=response["data"], status=response["status_code"])
    elif request.method == "POST":
        data = request.get_json()
        formatted_data = format_snake_case(data)
        response = goal_service.process_goal(formatted_data)
        return jsonify(data=response["data"], status=response["status_code"])


@app.errorhandler(CustomException)
def handle_custom_exception(error):
    return Response(status=error.status_code, response=error.message)
