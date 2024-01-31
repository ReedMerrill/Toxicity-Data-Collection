import calls
import json

# single sub for testing
seeds_dict = json.load(open('seed-subreddits.json'))
SEED_SUBREDDITS = seeds_dict['all']

def main():

    reddit = calls.setup_access()

    time_period = 'year'
    n_submissions = 10

    seed_to_posts = {}
    post_to_comments = {}
    comment_to_user = {}
    users = {'users': []}

    # iterate through the seed subreddits, getting a list of the IDs of top posts from each
    for seed in SEED_SUBREDDITS:

        posts = calls.get_top_posts(reddit=reddit, subreddit_name=seed, time_period=time_period, n_submissions=n_submissions)

        # add a key "seed" with the post IDs as items
        seed_to_posts.update({seed: posts})
        
        # iterate through the posts returned from the seed, retreiving their comment IDs
        for post in posts:

            comments = calls.get_post_comments_ids(reddit=reddit, submission_id=post)

            post_to_comments.update({post: comment})
            
            # iterate through the comments, retreiving each one's author
            for comment in comments:

                user = calls.get_comment_author(reddit=reddit, comment_id=comment)
                
                # add the new comment/user pair to the dict
                comment_to_user.update({comment: user})
                
                users['users'].append(user)
    
    output_dict = {
        'seed_to_posts': seed_to_posts,
        'post_to_comments': post_to_comments,
        'comment_to_user': comment_to_user
    }

    # output sampling procedure
    with open("sampling-prodecure.json", "w") as outfile: 
        json.dump(output_dict, outfile)
    
    # output users dict
    with open("user-sample.json", "w") as outfile: 
        json.dump(users, outfile)

if __name__ == "__main__":
    main()