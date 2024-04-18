# Multiply Coding Task

## Problem overview

At Multiply, we help people achieve their financial goals. In order to do this, we need ways to collect relevant information about people's goals. Under `api/models.py`, you will find a structure for the kind of information about people's goals which we want to collect alongside a simple structure to collect basic user information.

## Task

Your task is to use this repo a base to write a simple Python API which allows the registration of a user and storing of their goal information.

Create an API route, which will accept `POST` JSON requests to a `/user` route of the following form:

```javascript
POST /user:

{
  "first_name": "Jan",
  "email": "jan@multiply.ai"
}


```

Users should be stored in the `USER_STORE` dictionary, which has been instantiated for you under `api/api.py`. Make sure to validate incoming data however you see fit.

The API should then be able to accept `POST` and `GET` JSON requests of the following form to a `/goal` route:

```javascript
POST /goal:

{
  "goalId": "1234567890",
  "targetAmount": 100.00
}

{
  "goalType": "WEDDING",
  "targetAmount": 100.00
}

GET /goal:
{
  "goalId": "1234567890"
}

```

These goals should be stored in the `GOAL_STORE` dictionary.

We have provided you with a basic set up, which uses [Poetry](https://python-poetry.org/) to manage dependencies, and which uses [Flask](https://flask.palletsprojects.com/) to run the web server and [pytest](https://docs.pytest.org/) to run any tests. We suggest you build off this base. You can run the server in development mode using `poetry run flask run` and you can run all the tests using `poetry run pytest .`.

## API spec

- The API should accept camel case JSON bodies, which should be transformed to snake case serverside.
- `POST` requests to the `/user` route should create and persist a particular user. For this exercise, assume that this route cannot be used to update user information.
- `POST` requests sent to the `/goal` route should create and persist or update one or more fields. We would also like the response to indicate the `goal_id` for the Goal you have created/updated. Note that the list of possible requests above is not exhaustive. Think about all the different types of requests that we would like to `POST` to the `/goal` route.
- `GET` requests sent to the `/goal` route should return all the fields for a particular goal.
- The possible goal types your API should be prepared to handle are `WEDDING`, `HOMEBUYING`, `NEW_CAR` and `CUSTOM`.

Feel free to use any additional libraries you may need. README should contain details on how to install, run and test your code.

Good luck!
