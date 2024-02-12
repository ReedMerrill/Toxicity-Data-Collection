PROJECT_PATH = "/home/reed/Projects/learned-toxicity-reddit/reddit-api/"
INPUT_PATH = f"{PROJECT_PATH}data/user-sample.csv"
OUTPUT_PATH = f"{PROJECT_PATH}data/"

import pandas as pd
from reddit-api.src import utils

users = pd.read_csv(INPUT_PATH)

clean = utils.process_user_ids(users["users"])
