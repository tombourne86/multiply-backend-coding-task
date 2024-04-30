# Multiply Coding Task

## Tom's notes

### Building and running this branch

- Update poetry to install the following:
  - black
  - ruff
  - pre-commit
  - coverage
  - pyhamcrest
- run `pre-commit install` to install a git hook which runs some simple sense checks, ruff and black before a commit.
- to run tests with coverage, run: `coverage run && coverage report -m`
- otherwise, running a local flask server and executing the tests can be done as recommended below.

### API descriptions

#### /user:
  - Expects an input to contain two fields, a `firstName` and an `email`.
  - Accepts a camelcase input and converts input fields to snake case.
  - Invokes `user_service`.
  - Validates that only a `first_name` and an `email` are now present in the request body.
  - Validates that the `email` is formatted as an email address.
  - Validates that the email has not already been added to the `USER_STORE` (to prevent duplicate accounts).
  - For a validated request, calculates the next available `user_id` (simulating an incrementing index).
  - Creates a `User` object with the request data and `user_id`.
  - Adds user to `USER_STORE` with a key of the `user_id` and value of the `User` object.

#### /goal:
  - Expects an input to contain optionally a `goalId` or a `user`. This means:
    - we allow goals to be stored without an associated user (e.g. as 'templates')
    - a 'template' could be associated with a user in future as an update.
    - a goal assigned to a user can be updated, but the user details cannot, so an existing goal that is associated with a user cannot be reassigned to a new user.
    - the /goal api is not able to inadvertently update an existing user's details since responsibilities should be kept separate.
    - the passing of user data in an api call is reduced since this data is likely tp be sensitive.
    - NB: here the `Goal` model is used with the attributes provided, but a possible improvement to the design would be to have it use only a `user_id` rather than a `User` object containing data.
  - Also expects a request to contain at least one of: `goalType`, `targetDate` and `targetSum`.
  - Accepts a camelcase input and converts input fields to snake case.
  - Invokes `goal_service`.
  - Checks for a `goal_id` and if so removes it from input data (since `Goal` object doesn't have an id atribute)
  - Validates that any present `goal_id` exists in `GOAL_STORE`.
  - Validates that not both `goal_id` and `user` are present as described above.
  - Validates that only other fields in request have a matching attribute in `Goal` object.
  - Validates that any `goal_type` is a valid option.
  - Validates that date is of `YYYY-MM-DD` format and converts to `datetime.date` object.
  - Validates that any `user` present has correct fields.
  - Creates a `Goal` object.
  - If a `goal_id` was present, then attempts to update an existing item in `GOAL_STORE`
  - Otherwise, calculates the next available `goal_id`.
  - Attempts to add a new goal to `GOAL_STORE` with a key of the `goal_id` and value of the `Goal` object.


### Suggested improvements/Next steps

- Validation would be easier (especially the handling of optional attributes) if we used e.g. Pydantic for model building.
- Currently, /goal does not fully validate that a user exists etc. This would be a logical next step.
- The /goal api currently expects one goal per request, but it might be desirable to allow a user/advisor to create multiple goals at once.
- There are likely some edge cases and combinations that are not fully covered by the tests included here.
- As the app scaled, we would likely need separate custom exceptions for each feature. We may also need to handle validation in a separate class as requirements grew.
- Features and there corresponding tests would need separate folders as the app scaled.


### Other Notes

- While `USER_STORE` and `GOAL_STORE` dicts might be sufficient for the exercise, it is assumed that a production version would have a separate data persistence (e.g. a database).
- This would require a 'DAO' layer to be passed to the service class which would be responsible for connecting to the database and passing data back and forth.
- This layer would be tested with extensive mocking of the data persistence.
- Tests are not included in pre-commit since this can slow the process of committing down and therefore lead to larger, less-frequent commits. This would be undesirable when considering the aspiration of more frequent deployments.
- To convert camel to snake, a function is used here since regex can be complex/hard to maintain and the inflection library would create a fragile dependency for one relatively small piece of functionality.
- The conversion from camel to snake case might also be achieved using a decorator to wrap the api routes, rather than calling a method each time.


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
