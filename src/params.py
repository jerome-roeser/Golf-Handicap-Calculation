import os
from pathlib import Path


##################  VARIABLES  ##################
USER_NAME = os.environ.get('USER_NAME')
PASSWORD = os.environ.get('PASSWORD')
GOLFSHOT_URL = os.environ.get('GOLFSHOT_URL')
USER_ID = os.environ.get('USER_ID')
USER_UNTIL = os.environ.get('USER_UNTIL')


##################  PATHS  #####################
repo_path = Path(__file__).parent.parent

LOCAL_DATA_PATH = Path(repo_path).joinpath("data")

COURSES_DIRECTORY = Path(repo_path).joinpath("data", "courses")
ROUNDS_DIRECTORY = Path(repo_path).joinpath("data", "rounds")
