"""Take a subset of the sample of users generated in snowball.py (and stored
in data/sample/user-sample.py).
"""

PROJECT_PATH = "/home/reed/Projects/learned-toxicity-reddit/reddit-api/"
INPUT_PATH = (
    f"{PROJECT_PATH}data/comments/sample-subset/20pct-users-subset_comments.csv"
)
OUTPUT_PATH = f"{PROJECT_PATH}data/comments/"

import pandas as pd
import random
import utils

comments = pd.read_csv(INPUT_PATH)
# downsample by 50%
comments_subset = comments.sample(n=round(comments.shape[0] * 0.55), random_state=1)

print(f"Original N: {comments.shape[0]}, Subset Length: {comments_subset.shape[0]}")

out = pd.DataFrame(comments_subset, columns=["users"])

with open(f"{OUTPUT_PATH}10pct-users-subset_comments", "w") as file:
    out.to_csv(file, index=False)
