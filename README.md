Multiply Coding Task
====================

## Problem overview

At Multiply, we help people achieve their financial goals. In order to do this, we need ways to collect relevant information about people's goals. Under `api/models.py`, you will find a structure for kind of information about people's goals which we want to collect.

## Task

Your task is to write a simple Python API which allows the registration of a user and storing of their goal information.

Create an API route, which will accept `POST` JSON requests to a `/user` route of the following form:

```javascript
POST /user:

{
  "first_name": "Jan",
  "email": "jan@multiply.ai"
}


```

The requests should store the user in the `USER_STORE` dictionary, which has been instantiated for you under `api/api.py`. Make sure to validate the bodies of these requests in a way you see fit.

The API should then be able to accept `POST` and `GET` JSON requests of the following form to a `/goal` route:

```javascript
POST /goal:

{
  "goalType": "WEDDING",
  "targetAmount": 100.00
}

GET /goal
{
  "goalId": "1234567890"
}

```

Analogously, these goals should be stored in the `GOAL_STORE` dictionary.

Write the API using Flask or any other Python REST framework (Django/FastAPI/etc.) if you are more comfortable with that. Please push your work onto a separate branch.

Please test the code you write in the `tests` directory.


## API spec

* The API should accept camelcase JSON bodies, which should be transformed to snake case serverside. 
* `POST` requests sent to the `/goal` route should update one or more fields. We would also like the response to indicate the `goal_id` for the Goal you have created.
* The possible goal types your API should be prepared to handle are `WEDDING`, `HOMEBUYING`, `NEW_CAR` and `CUSTOM`