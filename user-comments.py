"""Takes '/output/user-sample.csv' as input and collects the last 1,000 comments made by each user.
"""
import asyncio
import pandas as pd
import calls

PROJECT_PATH = '/home/reed/Projects/learned-toxicity-reddit/reddit-api/'
INPUT_PATH = f'{PROJECT_PATH}/data/user-sample.csv'
OUTPUT_PATH = f'{PROJECT_PATH}data/'
users = pd.read_csv(INPUT_PATH)

async def main():

    reddit = await calls.setup_async_access()

    user_ids = await calls.process_user_ids(reddit, users['users'])

asyncio.run(main()) 