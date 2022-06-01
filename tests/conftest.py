import sys
from pathlib import Path
import pytest


sys.path.insert(0, str(Path(__file__).parent.parent / 'multiply_backend_coding_task'))


from main import app


@pytest.fixture(scope='session')
def test_client():

    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()
    with app.test_request_context('/'):
        yield testing_client
    ctx.pop()
