import os

DEBUG = False
PORT = 8000
SECRET_KEY = "abc123"
BASE_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(__file__)))

TEMPLATES_PATH = os.path.join(BASE_DIR, 'templates')
STATIC_PATH = os.path.join(BASE_DIR, 'static')

INFLUX = {
    'username': 'root',
    'password': 'root',
    'database': 'tank_maven',
}

