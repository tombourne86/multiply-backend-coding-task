import os
import sys


def start():
    print('\33]0;Multiply Test\a', end='')
    sys.stdout.flush()
    os.environ['FLASK_APP'] = 'multiply_backend_coding_task/main.py'
    os.environ['FLASK_ENV'] = 'development'
    os.system('poetry run flask run --port 8080')
