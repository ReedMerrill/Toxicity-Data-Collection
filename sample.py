"""A job script that samples Reddit users from an initial list of subreddits.
"""
import json
import time
import datetime
import sys
import calls

# single sub for testing
INPUT_PATH = '/home/reed/Projects/learned-toxicity-reddit/reddit-api/seed-subreddits.json'
OUTPUT_PATH = '/home/reed/Projects/learned-toxicity-reddit/reddit-api/output/'
SEEDS_DICT = json.load(open(INPUT_PATH))
#SEED_SUBREDDITS = seeds_dict['all']
SEED_SUBREDDITS = ['test']
LOG_DESC = 'testing'
LOG_FILE_PATH = [f'logs/{LOG_DESC}_{datetime.datetime()}.txt']

def main():
    """Iterate through the sampling structure, saving the elements used in sampling at each level.
    """

    start = time.time()

    print("Initializing API Instance")

    reddit = calls.setup_access()

    print("Initialization complete.")

    time_period = 'year'
    n_submissions = 1

    seed_to_posts = {}
    post_to_comments = {}
    comment_to_user = {}
    users = {'users': []}

    # iterate through the seed subreddits, getting a list of the IDs of top posts from each
    for seed in SEED_SUBREDDITS:

        posts = calls.get_top_posts(reddit=reddit, subreddit_name=seed, time_period=time_period,
                                    n_submissions=n_submissions)

        # add a key "seed" with the post IDs as items
        seed_to_posts.update({seed: posts})

        # iterate through the posts returned from the seed, retreiving their comment IDs
        for i, post in enumerate(posts):

            comments = calls.get_post_comments_ids(reddit=reddit, submission_id=post)

            post_to_comments.update({post: comments})

            # iterate through the comments, retreiving each one's author
            for j, comment in enumerate(comments):

                sys.stdout.flush()
                sys.stdout.write(
                    f'{datetime.datetime()} - Fetching:\n\tSeed: {seed}, Post: {i}, Comment: {j}')

                user = calls.get_comment_author(reddit=reddit, comment_id=comment)

                # add the new comment/user pair to the dict
                comment_to_user.update({comment: user})

                users['users'].append(user)

            with open(LOG_FILE_PATH, "a") as log_file:
                log_file.write(f'{datetime.datetime} - Finished Post {i} of seed "{seed}"')

    output_dict = {
        'seed_to_posts': seed_to_posts,
        'post_to_comments': post_to_comments,
        'comment_to_user': comment_to_user
    }

    # output sampling procedure
    with open(OUTPUT_PATH + "sampling-prodecure.json", "w") as outfile:
        json.dump(output_dict, outfile, indent=4)

    # output users dict
    with open(OUTPUT_PATH + "user-sample.json", "w") as outfile:
        json.dump(users, outfile, indent=4)

    finished = time.time()

    job_time = finished - start / 60

    print(f'Job took {job_time} minutes')

if __name__ == "__main__":
    main()
