"""Use civility-lab/roberta-base-namecalling to classify if Reddit comments
were namecalling.
"""

import json
import pandas as pd
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TextClassificationPipeline,
)

PROJECT_PATH = "/home/reed/Projects/learned-toxicity-reddit/reddit-api/"
INPUT_PATH = f"{PROJECT_PATH}data/comments/comments-testing.csv"
OUTPUT_PATH = f"{PROJECT_PATH}data/comments/classified-comments.json"

model_name = "civility-lab/roberta-base-namecalling"
classifier = TextClassificationPipeline(
    tokenizer=AutoTokenizer.from_pretrained(model_name),
    model=AutoModelForSequenceClassification.from_pretrained(model_name),
)

out = classifier(["suck it", "you suck"])
print(out)
