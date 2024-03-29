"""Which seed did each user originate from?"""

import json
import pandas as pd

DATA_DIR = (
    "/home/reed/Projects/learned-toxicity-reddit/toxicity-data-collection/data/sample/"
)
# load data
sampling_frame_dict = json.load(
    open(
        DATA_DIR + "sampling-procedure.json",
    )
)

# seed to posts
seed_to_posts = pd.DataFrame(sampling_frame_dict["seed_to_posts"])
seed_to_posts = seed_to_posts.T.reset_index()
# pivot wide to long
seed_to_posts = seed_to_posts.melt(id_vars="index", value_name="posts")
seed_to_posts = seed_to_posts.drop("variable", axis=1)
seed_to_posts.columns = ["seed", "post"]
seed_to_posts_df = seed_to_posts.sort_values("seed", ascending=False)

# posts to comments
# needs a different approach because each post has a different number of comments
post_to_comments_dict = sampling_frame_dict["post_to_comments"]

post_to_comments_df = pd.DataFrame({"post": [], "comment": []})
for key in post_to_comments_dict:
    key_col = [key] * len(post_to_comments_dict[key])
    df = pd.DataFrame([key_col, post_to_comments_dict[key]]).T
    df.columns = ["post", "comment"]
    post_to_comments_df = pd.concat([post_to_comments_df, df], axis=0)

# comments to users
# comments_to_users_df = pd.DataFrame(sampling_frame_dict["comment_to_user"])
comment_ids = list(sampling_frame_dict["comment_to_user"].keys())
user_ids = [sampling_frame_dict["comment_to_user"][comment] for comment in comment_ids]

# sanity checks
# are the two lists the same length?
assert len(comment_ids) == len(user_ids)
# are the comment ids unique?
assert len(list(set(comment_ids))) == len(comment_ids)

# create dataframe
comments_to_users_df = pd.DataFrame({"comment": comment_ids, "user": user_ids})
# keep only unique rows
comments_to_users_df = comments_to_users_df.drop_duplicates("user")


# verify that the number of unique users is the same in the final dataframe
assert len(list(set(user_ids))) == comments_to_users_df.shape[0]

# =============================================================================
# merge dataframes
# =============================================================================

# type conversions
comments_to_users_df["comment"] = comments_to_users_df["comment"].astype(str)
post_to_comments_df["comment"] = post_to_comments_df["comment"].astype(str)
seed_to_posts_df["post"] = seed_to_posts_df["post"].astype(str)

# merge comments to users
comments_to_posts_df = comments_to_users_df.merge(
    post_to_comments_df, on="comment", how="left", validate="m:1"
)

# merge posts to comments
users_to_seeds_df = comments_to_posts_df.merge(
    seed_to_posts_df, on="post", how="left", validate="m:1"
)

assert users_to_seeds_df.shape[0] == len(list(set(user_ids)))

with open(DATA_DIR + "user-seed-lookup.csv", "w") as f:
    users_to_seeds_df.to_csv(f, index=False)
