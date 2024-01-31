import praw
import json

# credentials
CLIENT_ID = "gB_we0e6sW9IK_Xjrw1szQ"
CLIENT_SECRET = "6rDRP5Hfu6SykadFTDZ8BMi4zSQNUg"
PASSWORD = "CmhtIf!rc-6ZmoJ"
USER_AGENT = "Reed's politics scraper v1.0.0 (u/bewchacca-lacca)"
USERNAME = "bewchacca-lacca"

# single sub for testing
seeds_dict = json.load(open('seed-subreddits.json'))
SEED_SUBREDDITS = seeds_dict['all']

def setup_access():
    """Create an instance for API access"""
    instance = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=PASSWORD,
        user_agent=USER_AGENT,
        username=USERNAME)
    return instance


def get_posts(reddit, subreddit_name, time_period, n_submissions):
    """Takes the name of a subreddit, a time period, and the desired number of submissions
    and returns a list of the URLs of that subreddit's top posts.
    
    nb this is a separate function because doing so retains a list of the submissions, and parsing
    each level of the user extraction process into its own function avoids messy function outputs
    and is more efficient.
    Returns: list of top post URLs
    """
    
    # create the generator
    submission_generator = reddit.subreddit(subreddit_name).top(time_filter=time_period, limit=n_submissions)
    # return generator outputs as a list
    return [submission.id for submission in submission_generator]
    

def get_post_comments_ids(reddit, submission_id):
    """Takes a list of submission URLs and returns a (flattened) list of all its comments.
    """
    # create a post instance
    comments = reddit.submission(submission_id).comments
    # replace_more() updates the comment forest by resolving instances of MoreComments
    comments.replace_more()
    # list flattens the comment forest to a simple list of comments, extracting all comment replies
    return [comment.id for comment in comments.list()]

def main():

    reddit = setup_access()

    time_period = 'year'
    n_submissions = 10

    seed_to_posts = {}
    post_to_comments = {}
    comment_to_user = {}
    users = {'users': []}

    # iterate through the seed subreddits, getting a list of the IDs of top posts from each
    for seed in SEED_SUBREDDITS:

        posts = get_posts(reddit=reddit, subreddit_name=seed, time_period=time_period, n_submissions=n_submissions)

        # initialize the output dict and add a key "seed" with items being post IDs
        seed_to_posts.update({seed: posts})
        
        # iterate through the posts returned from the seed, retreiving their comment IDs
        for post in posts:

            comments = get_post_comments_ids(reddit=reddit, submission_id=post)

            post_to_comments.update({post: comment})
            
            # iterate through the comments, retreiving each one's author
            for comment in comments:

                # retreived the author of each comment
                user = reddit.comment(comment).author
                
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