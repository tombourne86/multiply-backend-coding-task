from flask import Flask

app = Flask(__name__)


USER_STORE = {}
GOAL_STORE = {}


@app.route('/')
def hello_world():
    return 'Hello, world!'
