import pandas as pd
import utils

PROJECT_PATH = "/home/reed/Projects/learned-toxicity-reddit/toxicity-data-collection/"
INPUT_PATH = f"{PROJECT_PATH}data/comments/11pct-users-subset_comments.csv"
OUTPUT_PATH = f"{PROJECT_PATH}data/comments/11pct-users-subset_comments_CLEAN.csv"

data = pd.read_csv(INPUT_PATH, encoding="utf-8")

data["text"] = data["text"].map(utils.remove_emojis)
data["text"] = data["text"].map(utils.remove_urls)
data["text"] = data["text"].map(utils.check_language)

data = data.dropna(subset=["text"], axis=0)

data.to_csv(OUTPUT_PATH, index=False)
