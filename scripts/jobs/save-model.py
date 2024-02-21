"""Use s-nlp/roberta_toxicity_classifier to classify if Reddit comments
were toxic.

Run in transformers env (from transformers.yml)
"""

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TextClassificationPipeline,
)

PROJECT_PATH = "/home/reed/Projects/learned-toxicity-reddit/reddit-api/"
OUTPUT_PATH = f"{PROJECT_PATH}scripts/jobs/"

model_name = "s-nlp/roberta_toxicity_classifier"

classifier = TextClassificationPipeline(
    tokenizer=AutoTokenizer.from_pretrained(model_name, truncate=True),
    model=AutoModelForSequenceClassification.from_pretrained(model_name),
)

classifier.model.save_pretrained(f"{OUTPUT_PATH}roberta_toxicity_classifier")
