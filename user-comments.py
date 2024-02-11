"""Takes output/user-sample.json as input and collects the last 1,000 comments made by each user.
"""
import asyncio
import json
import calls

INPUT_PATH = '/home/reed/Projects/learned-toxicity-reddit/reddit-api/data/user-sample.json'
OUTPUT_PATH = '/home/reed/Projects/learned-toxicity-reddit/reddit-api/data/user-comments/'
users_dict = json.load(open(INPUT_PATH))

reddit = calls.setup_async_access()

user_ids = calls.process_user_ids(reddit, users_dict['users'])

async def main():
    """"""

    return None
    
asyncio.run(main()) 