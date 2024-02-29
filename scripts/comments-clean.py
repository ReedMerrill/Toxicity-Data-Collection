import pandas as pd
import utils

PROJECT_PATH = "/home/reed/Projects/learned-toxicity-reddit/toxicity-data-collection/"
INPUT_PATH = f"{PROJECT_PATH}data/comments/15pct-users-subset_comments.csv"
OUTPUT_PATH = f"{PROJECT_PATH}data/comments/15pct-users-subset_comments_CLEAN.csv"

data = pd.read_csv(INPUT_PATH)

print("Removing Emojis...")
data["text"] = data["text"].map(utils.remove_emojis)
print("Removing URLs...")
data["text"] = data["text"].map(utils.remove_urls)
print("checking language...")
data["text"] = data["text"].map(utils.check_language)

data = data.dropna(subset=["text"], axis=0)

print("writing output csv...")
data.to_csv(OUTPUT_PATH, index=False)
