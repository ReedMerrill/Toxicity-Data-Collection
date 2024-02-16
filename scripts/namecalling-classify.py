"""Use civility-lab/roberta-base-namecalling to classify if Reddit comments
were namecalling.

Run in transformers env (from transformers.yml)
"""

import json
import time
import pandas as pd
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TextClassificationPipeline,
)

PROJECT_PATH = "/home/reed/Projects/learned-toxicity-reddit/reddit-api/"
INPUT_PATH = f"{PROJECT_PATH}data/comments/20pct-users-subset_comments.csv"
OUTPUT_PATH = f"{PROJECT_PATH}data/comments/classified-comments.json"

model_name = "civility-lab/roberta-base-namecalling"
classifier = TextClassificationPipeline(
    tokenizer=AutoTokenizer.from_pretrained(model_name, truncate=True),
    model=AutoModelForSequenceClassification.from_pretrained(model_name),
)


def main():

    data = pd.read_csv(INPUT_PATH)
    text_list = list(data["text"])

    start = time.time()

    # classifier is a ListingGenerator, so it does the iteration automatically
    out = classifier(text_list, truncation=True, max_length=512)
    output_dict = {}
    output_dict["label"] = [item["label"] for item in out]  # ignore linting

    with open(OUTPUT_PATH, "w") as file:
        json.dump(output_dict, file)

    # log time elapsed
    print(f"Time Elapsed: {time.time() - start}")


if __name__ == "__main__":
    main()
