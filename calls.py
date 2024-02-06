"""A collection of wrappers for PRAW.
"""
import time
import praw
from prawcore.exceptions import TooManyRequests


# credentials
CLIENT_ID = "gB_we0e6sW9IK_Xjrw1szQ"
CLIENT_SECRET = "6rDRP5Hfu6SykadFTDZ8BMi4zSQNUg"
PASSWORD = "CmhtIf!rc-6ZmoJ"
USER_AGENT = "Reed's politics scraper v1.0.0 (u/bewchacca-lacca)"
USERNAME = "bewchacca-lacca"

def setup_access():
    """Create an instance for API access"""
    instance = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=PASSWORD,
        user_agent=USER_AGENT,
        username=USERNAME)
    return instance


def get_top_posts(reddit, subreddit_name, time_period, n_submissions):
    """Takes the name of a subreddit, a time period, and the desired number of submissions
    and returns a list of the URLs of that subreddit's top posts.
    
    nb this is a separate function because doing so retains a list of the submissions, and parsing
    each level of the user extraction process into its own function avoids messy function outputs
    and is more efficient.
    Returns: list of top post URLs
    """
    # create the generator
    submission_generator = reddit.subreddit(subreddit_name).top(time_filter=time_period,
                                                                limit=n_submissions)
    # return generator outputs as a list
    return [submission.id for submission in submission_generator]
    

def get_post_comments_ids(reddit, submission_id):
    """Takes a submission ID and returns a (flattened) list of all its comments.
    """
    # create a post instance
    comments = reddit.submission(submission_id).comments
    # replace_more() updates the comment forest by resolving instances of MoreComments
    comments.replace_more()
    # list() flattens the comment forest to a simple list of all comments on the submission
    return [comment.id for comment in comments.list()]


def get_comment_author(reddit, comment_id):
    """Takes a comment ID and return that comment's author.
    """
    return str(reddit.comment(comment_id).author)


def process_user_ids(id_list):
    """Clean the user IDs obtained during runs of sample.py.

    Inputs: list of user IDs
    Returns: Cleaned list of user IDs
        - removes duplicates
        - removes AutoModerator
        - removes None values
    """
    no_dupes = list(set(id_list))

    return [user for user in no_dupes if user not in ("None", "AutoModerator")]

def log_to_file(name, message):
    """output logging events to a file
    """
    with open(f'logs/{name}.txt', 'a') as file:
        file.write(message)

def get_user_comments(reddit, user_id, limit=1000, log_name='log'):
    """Takes a user ID and collects up to 1,000 of that user's most recent comments, with metadata.
    Filters "distinguished" comments, which are used to add a "MOD" decorator (used when engaging
    as a moderator rather than a community member).
    """

    # logging
    log_name = log_name

    # get a ListingGenerator for up to the user's 1,000 most recent comments
    user_comment_generator = reddit.redditor(user_id)

    user_comments = {}

    # iterate over the generator, calling each item
    for i, comment in enumerate(user_comment_generator.comments.new(limit=limit)):

        # logging
        print(f'Fetching user {i + 1}')

        # initialize try/except vars
        n_retries = 0 # retry counter
        sleep_time = 0 # retry sleep time

        # retry loop
        while n_retries < 4:
            try:
                # Main block: fetch comment metadata
                # don't collect distinguished comments
                if comment.distinguished != 'moderator':

                    # data to collect
                    comment_metadata = {
                        'comment_id': comment.id,
                        'post_id': comment.link_id,
                        'subreddit_id': comment.subreddit_id,
                        'timestamp': comment.created_utc,
                        'text': comment.body,
                        'upvotes': comment.score,
                        'parent_comment': comment.parent_id # if top-level, then returns the submission ID
                        }

                    user_comments.update({comment.id: comment_metadata})

            # if a TooManyRequsts error is raised then the API rate limit has been exceeded.
            # Retry after sleeping. Sleep duration increases by a factor of 2 for 4 retries, and then gives up.
            except TooManyRequests as e:
                log_to_file(log_name, f'Error: {e} while fetching user {i + 1}')
                print(f'Error: {e} while fetching user {i + 1}')

                if n_retries == 0:
                    sleep_time = 1
                    print(f'Retry: {n_retries + 1} with {sleep_time}s sleep')
                    time.sleep(sleep_time)
                    n_retries += 1

                if n_retries == 1:
                    sleep_time *= 2
                    print(f'Retry: {n_retries + 1} with {sleep_time}s sleep')
                    time.sleep(sleep_time)
                    n_retries += 1

                if n_retries == 2:
                    sleep_time *= 2
                    print(f'Retry: {n_retries + 1} with {sleep_time}s sleep')
                    time.sleep(sleep_time)
                    n_retries += 1
                    sleep_time *= 2
                    
                if n_retries == 3:
                    sleep_time *= 2
                    print(f'Retry: {n_retries + 1} with {sleep_time}s sleep')
                    time.sleep(sleep_time)
                    n_retries += 1

            # catch all other possible exceptions
            except Exception as e:
                log_to_file(log_name, f'Unresolved Error: "{e}" while fetching user {i + 1}')
                print(f'Error: {e} while fetching user {i + 1}')
                # set to 4 so the try loop stops
                n_retries = 4
                
    return user_comments
