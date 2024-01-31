"""A job script that samples Reddit users from an initial list of subreddits.
"""
import json
import time
import calls

# single sub for testing
INPUT_PATH = '/home/reed/Projects/learned-toxicity-reddit/reddit-api/seed-subreddits.json'
OUTPUT_PATH = '/home/reed/Projects/learned-toxicity-reddit/reddit-api/output/'
seeds_dict = json.load(open(INPUT_PATH))
SEED_SUBREDDITS = seeds_dict['all']

def main():
    """Iterate through the sampling structure, saving the elements used in sampling at each level.
    """

    start = time.time()

    reddit = calls.setup_access()

    time_period = 'year'
    n_submissions = 10

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

                print(f'Fetching Author:\n\tPost: {i}\n\tComment: {j}\n\tSeed: {seed}')

                user = calls.get_comment_author(reddit=reddit, comment_id=comment)

                # add the new comment/user pair to the dict
                comment_to_user.update({comment: user})

                users['users'].append(user)

        print(f'Finished: {seed}')

    output_dict = {
        'seed_to_posts': seed_to_posts,
        'post_to_comments': post_to_comments,
        'comment_to_user': comment_to_user
    }

    # output sampling procedure
    with open(OUTPUT_PATH + "sampling-prodecure.json", "w") as outfile:
        json.dump(output_dict, outfile)

    # output users dict
    with open(OUTPUT_PATH + "user-sample.json", "w") as outfile:
        json.dump(users, outfile)

    finished = time.time()

    job_time = finished - start

    print(f'Completion Time: {job_time}s')

if __name__ == "__main__":
    main()
