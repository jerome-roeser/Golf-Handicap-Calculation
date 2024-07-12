import os
from pathlib import Path


##################  VARIABLES  ##################
USER_NAME = os.environ.get('USER_NAME')
PASSWORD = os.environ.get('PASSWORD')
GOLFSHOT_URL = os.environ.get('GOLFSHOT_URL')
USER_ID = os.environ.get('USER_ID')
USER_UNTIL = os.environ.get('USER_UNTIL')


##################  CONSTANTS  #####################
repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCAL_DATA_PATH = os.path.join(repo_path, "data")
LOCAL_REGISTRY_PATH =  os.path.join(repo_path, ".lewagon", "mlops", "training_outputs")

COURSES_DIRECTORY = os.path.join(repo_path, "data", "courses")
ROUNDS_DIRECTORY = os.path.join(repo_path, "data", "rounds")
