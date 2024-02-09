"""Takes '/output/user-sample.csv' as input and collects each user's recent comments.
"""

import time
from datetime import datetime
import json
import pandas as pd
import calls
import utils

PROJECT_PATH = "/home/reed/Projects/learned-toxicity-reddit/reddit-api/"
INPUT_PATH = f"{PROJECT_PATH}/data/user-sample.csv"
OUTPUT_PATH = f"{PROJECT_PATH}data/"
COMMENT_LIMIT = 1000


def main():
    """Gets an API instance, cleans the usernames, fetches all comments for
    each user, then fetches each comment's metadata.
    """
    # initialize log file
    start_time = time.time()
    log_name = f"user-comment-extraction_{datetime.now()}"
    utils.log_to_file(log_name, f"{datetime.now()} - Begin Fetching comments...\n")
    # setup a PRAW reddit instance
    reddit = calls.setup_access()
    print("API Authentication Successful")
    # read in users list
    users = pd.read_csv(INPUT_PATH)
    # remove duplicate users and moderators
    users_list = utils.process_user_ids(list(users["users"]))
    # iterate over list of user, extracting each user's comment metadata
    user_comment_data = {}
    for i, user in enumerate(users_list):
        # initialize dict to store a single user's comments
        user_comments = {}
        # call for comment metadata from API
        comments = calls.get_user_comments(
            reddit=reddit, user_id=user, limit=COMMENT_LIMIT, log_name=log_name
        )
        # add user comments to, mapping them to the username
        user_comments.update({user: comments})
        # add user comments dictionary to the dict of all user's comments
        user_comment_data.update(user_comments)
        # log finish time estimate
        estimate = utils.estimate_time_remaining(
            task_index=i, total_tasks=len(users_list), start_time=start_time
        )
        utils.log_to_file(log_name, f"Finished collecing data for User {i + 1}\n")
        utils.log_to_file(log_name, f"Time remaining: ~{estimate} hours\n")
    # output the data to JSON
    with open(OUTPUT_PATH + "user-comments.json", "w") as file:
        json.dump(user_comment_data, file, indent=4)
    # final logging
    total_time_hours = (time.time() - start_time) / 3600
    utils.log_to_file(log_name, f"Total Time Elapsed: {total_time_hours}\n")


if __name__ == "__main__":

    main()
