"""
The raw comments data maps user to comment IDs, and comment IDs to their meta-
data, including the comment's text.

From the raw comments data:

1. Extract a mapping of users to their comment IDs
2. Extract a mapping of comment metadata to comment IDs
3. Join these mappings into long format data, with each row being a comment.

Input: JSON format comments data t

Return:
"""

PROJECT_PATH = "/home/reed/Projects/learned-toxicity-reddit/reddit-api/"
INPUT_PATH = f"{PROJECT_PATH}data/comments/user-comments.json"
OUTPUT_PATH = f"{PROJECT_PATH}data/comments/comments-long.csv"

import json

comments_data = json.load(open(INPUT_PATH))

# 1. Extract a mapping of users to their comment IDs
users_to_comments = {}
for user, comments in comments_data.items():
    users_to_comments[user] = list(comments.keys())

# 2. Extract a mapping of comment metadata to comment IDs
comments_to_metadata = {}
for user, comments in comments_data.items():
    for comment, metadata in comments.items():
        comments_to_metadata[comment] = metadata
