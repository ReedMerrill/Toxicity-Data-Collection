# Toxicity on Reddit -- Data Collection

This code is part of a broader project to measure the over-time evolution of toxic behavior by politically engaged Reddit users. It carries a snowball sampling of Reddit comments, collects the metadata of the commenters, and labels the comments as toxic or not.

## Snowball Sampling

1,056,661 Reddit comments by 1,964 Reddit users were collected by first seeding a snowball sampling procedure with 11 subreddits. Then, a list of every user that had commented on the top 3 posts from within the last year for each of these subreddits was generated. Finally, 10.5% of users were randomly sampled from the larger list of users, and each of these users' last 1,000 comments were collected.
