PROJECT_PATH = '/home/reed/Projects/learned-toxicity-reddit/reddit-api/'
INPUT_PATH = f'{PROJECT_PATH}data/user-sample.csv'
OUTPUT_PATH = f'{PROJECT_PATH}data/'

import json
import calls

reddit = calls.setup_access()

user = 'noyoto'

comments = calls.get_user_comments(reddit=reddit, user_id=user, limit=10)

with open(OUTPUT_PATH + "comment-extraction-test.json", "w") as outfile:
    json.dump(comments, outfile, indent=4)

