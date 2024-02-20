"""Use s-nlp/roberta_toxicity_classifier to classify if Reddit comments
were toxic.

Run in transformers env (from transformers.yml)
"""

import os
import time
import pandas as pd
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TextClassificationPipeline,
)
import utils

PROJECT_PATH = "/home/reed/Projects/learned-toxicity-reddit/reddit-api/"
INPUT_PATH = f"{PROJECT_PATH}data/comments/20pct-users-subset_comments.csv"
OUTPUT_PATH = f"{PROJECT_PATH}data/comments/toxicity-classified-comments.csv"

model_name = "s-nlp/roberta_toxicity_classifier"

classifier = TextClassificationPipeline(
    tokenizer=AutoTokenizer.from_pretrained(model_name, truncate=True),
    model=AutoModelForSequenceClassification.from_pretrained(model_name),
)

# clean up before rerun
if os.path.exists(OUTPUT_PATH):
    os.remove(OUTPUT_PATH)
    print(f"A pre-existing output file has been successfully deleted.")


def batch_list(comments_list, batch_size):
    # create batches
    return [
        comments_list[i : i + batch_size]
        for i in range(0, len(comments_list), batch_size)
    ]


def main():
    data = pd.read_csv(INPUT_PATH)
    comments = data["comment_id", "text"]
    data["text"] = data["text"].map(utils.clean_comment)
    data["text"] = data["text"].map(utils.remove_emojis)
    start = time.time()

    for i in range(0, data.shape[0], 64):
        # index the next batch of text (row, col)
        batch_text = data.iloc[i : i + 64, 1]
        # get batches of comment ids
        batch_comment_ids = data.iloc[i : i + 64, 0]
        # do the batching
        out = classifier(batch_text, truncation=True, max_length=512)

        # streaming output to CSV
        # Extract labels and scores into separate lists
        label = [o["label"] for o in out]
        score = [o["score"] for o in out]

        # define header and attach output
        data_batch = pd.DataFrame(
            {
                "toxicity_label": label,
                "toxicity_score": score,
            }
        )
        # maybe just do a join of the ids back onto the toxicity labels now?

        file_exists = True if os.path.exists(OUTPUT_PATH) else False
        if file_exists is False:
            with open(OUTPUT_PATH, "w") as file:
                data_batch.to_csv(file, index=False, header=True)
        else:
            with open(OUTPUT_PATH, "a") as file:
                data_batch.to_csv(file, index=False, header=False)

        # logging
        print(f"Comments labelled: {(i + 1 * 64)}")
        estimate = utils.estimate_time_remaining(i, len(comment_batch_list), start)
        print(f"Time remaining: ~{estimate} hours")

    # log time elapsed
    print(f"Time Elapsed: {time.time() - start}")


if __name__ == "__main__":
    main()
