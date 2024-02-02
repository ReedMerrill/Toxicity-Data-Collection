import praw
import asyncpraw

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

async def setup_async_access():
    """Create an instance for API access"""
    instance = asyncpraw.Reddit(
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
    submission_generator = reddit.subreddit(subreddit_name).top(time_filter=time_period, limit=n_submissions)
    # return generator outputs as a list
    return [submission.id for submission in submission_generator]
    

def get_post_comments_ids(reddit, submission_id):
    """Takes a submission ID and returns a (flattened) list of all its comments.
    """
    # create a post instance
    comments = reddit.submission(submission_id).comments
    # replace_more() updates the comment forest by resolving instances of MoreComments
    comments.replace_more()
    # list flattens the comment forest to a simple list of comments, extracting all comment replies
    return [comment.id for comment in comments.list()]

    # retreived the author of each comment
def get_comment_author(reddit, comment_id):
    """Takes a comment ID and return that comment's author.
    """
    return str(reddit.comment(comment_id).author)

def get_comment_metadata(reddit, comment_id):
    """TODO: get all the comment metadata needed for the main analysis"""

    return None

def process_user_ids(id_list):
    """Clean the user IDs obtained during runs of sample.py.

    Inputs: list of user IDs
    Returns: Cleaned list of user IDs
        - removes duplicates
        - removes None values
    """

    no_dupes = list(set(id_list))

    return [user for user in no_dupes if user != "None"]

async def get_user_comments(reddit, user_id):
    """Takes a user ID and collects all of that user's comments.
    """

    return reddit.redditor(user_id).comments.new(limit=None)
