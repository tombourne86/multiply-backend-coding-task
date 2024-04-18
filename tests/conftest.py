import sys
from pathlib import Path
import pytest


from multiply_backend_coding_task.api import app


@pytest.fixture(scope='session')
def test_client():

    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()
    with app.test_request_context('/'):
        yield testing_client
    ctx.pop()
