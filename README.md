# ❗️ Toxicity on Reddit -- Data Collection

This code feeds into a broader project that will measure the over-time evolution of toxic behavior by politically engaged Reddit users. It carries out a snowball sampling of Reddit comments, collects the metadata of the commenters, and labels the comments as toxic or not.

## Snowball Sampling

1,056,661 Reddit comments by 1,964 Reddit users were collected by seeding a snowball sampling procedure with 11 subreddits. A list of every user that had commented on the top 3 posts of any of these seeds was generated. Then, 11% of those commenters were randomly sampled and each of these users' last 1,000 comments were collected. Each comment's text, timestamp, unique ID, commenter, parent post, parent comment, karma, and subreddit were collected.

## Toxicity Labels

After cleaning and verification to remove URLs, emojis, and comments without any linguistic tokens, the data was classified using a fine-tune of [RoBERTa](https://arxiv.org/abs/1907.11692) by [s-nlp](https://huggingface.co/s-nlp) ([s-nlp/roberta_toxicity_classifier](https://huggingface.co/s-nlp/roberta_toxicity_classifier)).

## User Metadata

User metadata that will facilitate later analysis of commenting behavior was also collected -- namely, the timestamp of when each commenter joined Reddit, and their their overall karma.

## Data Availability

As data is collected it will be added [here](https://drive.google.com/drive/folders/1H35tIGU3W619wB-TgLIaQqEp4RDXkOQZ?usp=drive_link).
