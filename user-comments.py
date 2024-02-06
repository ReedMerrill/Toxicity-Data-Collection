"""Takes '/output/user-sample.csv' as input and collects each user's recent comments.
"""
import pandas as pd
import calls

PROJECT_PATH = '/home/reed/Projects/learned-toxicity-reddit/reddit-api/'
INPUT_PATH = f'{PROJECT_PATH}/data/user-sample.csv'
OUTPUT_PATH = f'{PROJECT_PATH}data/'

# read in users list
users = pd.read_csv(INPUT_PATH)

def main():
    """Gets an API instance, cleans the usernames, fetches all comments for each user, then fetches
    each comment's metadata.
    """


if __name__ == "__main__":
    main()
