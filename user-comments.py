"""Takes '/output/user-sample.csv' as input and collects each user's recent comments.
"""
import time
import json
import pandas as pd
import calls

PROJECT_PATH = '/home/reed/Projects/learned-toxicity-reddit/reddit-api/'
INPUT_PATH = f'{PROJECT_PATH}/data/user-sample.csv'
OUTPUT_PATH = f'{PROJECT_PATH}data/'

def main():
    """Gets an API instance, cleans the usernames, fetches all comments for each user, then fetches
    each comment's metadata.
    """
    # initialize log file
    start = time.time()
    log_name = f'user-comment-extraction_{time.time()}'
    calls.log_to_file(log_name, f'{start} - Begin Fetching comments...')

    # setup a PRAW reddit instance
    reddit = calls.setup_access()
    print('API Authentication Successful')
    # read in users list
    users = pd.read_csv(INPUT_PATH)
    # Clean list of users for duplicates and mods
    users_list = calls.process_user_ids(list(users['users'])) 

    # iterate over list of user, extracting each user's comment metadata
    user_comment_data = {}
    for i, user in enumerate(users_list):

        # logging
        print(f'Fetching user {i + 1}')

        # initialize dict to store a single user's comments
        user_comments = {}
        # call for comment metadata from API
        comments = calls.get_user_comments(reddit=reddit, user_id=user,
                                           limit=1000, log_name=log_name)
        # add user comments to, mapping them to the username
        user_comments.update({user: comments})
        # add user comments dictionary to the dict of all user's comments
        user_comment_data.update(user_comments)

        # progress: terminal logging
        total_time = time.time() - start
        print(f'Finished User {i + 1}. Took {total_time}s')

    with open(OUTPUT_PATH + 'user-comments.json', 'w') as file:
        json.dump(user_comment_data, file, indent=4)

if __name__ == "__main__":

    main()

