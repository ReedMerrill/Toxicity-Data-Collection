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
INPUT_PATH = f"{PROJECT_PATH}data/comments/10pct-users-subset_comments.csv"
OUTPUT_PATH = f"{PROJECT_PATH}data/comments/toxicity-classified-comments.csv"

model_name = "s-nlp/roberta_toxicity_classifier"

classifier = TextClassificationPipeline(
    tokenizer=AutoTokenizer.from_pretrained(model_name, truncate=True),
    model=AutoModelForSequenceClassification.from_pretrained(model_name),
)

# clean up before rerun
if os.path.exists(OUTPUT_PATH):
    os.remove(OUTPUT_PATH)
    print(f"A pre-existing output file has been deleted.")


def batch_df(comments_df, batch_size):
    """Takes a DF and returns a list of DFs that are slices of the original,
    each with batch_size number of rows."""
    n_rows = comments_df.shape[0]
    batches = []
    for i in range(0, n_rows, batch_size):
        batch = [comments_df.iloc[i : i + batch_size, :]]
        batches.append(batch)

    return batches


def main():
    data = pd.read_csv(INPUT_PATH)
    print("++++++++++++++++++")
    print(data.columns)
    data["text"] = data["text"].map(utils.clean_comment)
    data["text"] = data["text"].map(utils.remove_emojis)
    comments_df = data["comment_id", "text"]
    start = time.time()

    batches_list = batch_df(comments_df=comments_df, batch_size=4)

    # loop over the batches in batches_list
    for batch in batches_list:

        comment_ids = batch["comment_id"]
        comments_text = list(batch["text"])
        out = classifier(comments_text, truncation=True, max_length=512)
        print(out)
        # streaming output to CSV
        # Extract labels and scores into separate lists. Need lists to make df
        label = [o["label"] for o in out]
        score = [o["score"] for o in out]

        # define header and attach output
        data_batch = pd.DataFrame(
            {
                "comment_id": comment_id,
                "toxicity_label": label,
                "toxicity_score": score,
            }
        )

        file_exists = True if os.path.exists(OUTPUT_PATH) else False
        if file_exists is False:
            with open(OUTPUT_PATH, "w") as file:
                data_batch.to_csv(file, index=False, header=True)
        else:
            with open(OUTPUT_PATH, "a") as file:
                data_batch.to_csv(file, index=False, header=False)

        # logging
        print(f"Comments labelled: {(index + 1 * 64)}")
        estimate = utils.estimate_time_remaining(index, len(batches_list), start)
        print(f"Time remaining: ~{estimate} hours")

        # log time elapsed
        print(f"Time Elapsed: {time.time() - start}")


if __name__ == "__main__":
    main()
