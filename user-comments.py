"""Takes '/output/user-sample.csv' as input and collects each user's recent comments.
"""
import pandas as pd
import calls

PROJECT_PATH = '/home/reed/Projects/learned-toxicity-reddit/reddit-api/'
INPUT_PATH = f'{PROJECT_PATH}/data/user-sample.csv'
OUTPUT_PATH = f'{PROJECT_PATH}data/'
users = pd.read_csv(INPUT_PATH)

def main():
    """Gets an API instance, cleans the usernames, fetches all comments for each user, then fetches
    each comment's metadata.
    """
    # get reddit API instance
    reddit = calls.setup_async_access()
    # remove duplicate usernames and 'None' values
    user_ids = calls.process_user_ids(reddit, users['users'])
    # retrieve each user's recent comments, up to 1,000 as per Reddit's maximum
    all_comments = {}

    def comments_wrapper():
        for user in user_ids:
            comments = calls.get_user_comments(reddit=reddit, user_id=user)
            all_comments.udate({user: comments})

main()
