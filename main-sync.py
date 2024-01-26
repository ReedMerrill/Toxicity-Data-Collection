import pprint
import praw

CLIENT_ID = "gB_we0e6sW9IK_Xjrw1szQ"
CLIENT_SECRET = "6rDRP5Hfu6SykadFTDZ8BMi4zSQNUg"
PASSWORD = "CmhtIf!rc-6ZmoJ"
USER_AGENT = "Reed's politics scraper v1.0.0 (u/bewchacca-lacca)"
USERNAME = "bewchacca-lacca"

def create_instance():
    """Create an instance for API access"""
    instance = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=PASSWORD,
        user_agent=USER_AGENT,
        username=USERNAME
    )
    return instance

reddit = create_instance()

subreddit = reddit.subreddit("neovim")

print(subreddit.display_name)
print("+++++++++++++++++++++++++++++++++++")
print(subreddit.title)
print("+++++++++++++++++++++++++++++++++++")
print(subreddit.description)

# get redditor info
my_reddit = reddit.redditor("bewchacca-lacca")

print("+++++++++++++++++++++++++++++++++++")
print(my_reddit.link_karma) # you have to print something to trigger a request and make the object non-lazy
pprint.pprint(vars(my_reddit))

# get a user subreddit
user_subreddit = reddit.subreddit('u_bewchacca-lacca')

print("+++++++++++++++++++++++++++++++++++")
print(user_subreddit.title) # the title field is empty
pprint.pprint(vars(user_subreddit))

# get a redditor's comments and submissions?
user_comments = reddit.redditor("bewchacca-lacca").comments.new(limit=None)
user_comments_list = list(user_comments)

print("+++++++++++++++++++++++++++++++++++")
print(user_comments_list[10]) # returns comment ID
print(len(user_comments_list))