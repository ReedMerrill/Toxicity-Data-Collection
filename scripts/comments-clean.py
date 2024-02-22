import pandas as pd
import utils

PROJECT_PATH = "/home/reed/Projects/learned-toxicity-reddit/reddit-api/"
INPUT_PATH = f"{PROJECT_PATH}data/comments/10pct-users-subset_comments.csv"
OUTPUT_PATH = f"{PROJECT_PATH}data/comments/toxicity-classified-comments.csv"

# data = pd.read_csv(INPUT_PATH)

data = pd.DataFrame(
    {
        "text": [
            "😆 clean",
            "https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url clean",
            "Merhaba seni seviyorum.",
        ]
    }
)

print("Dirty data")
print(data)

data["text"] = data["text"].map(utils.remove_emojis)
data["text"] = data["text"].map(utils.remove_urls)
data["text"] = data["text"].map(utils.check_language)

# data = data.dropna(subset=["text"], axis=0)

print("Clean data")
print(data)
