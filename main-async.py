import asyncpraw

CLIENT_ID = "gB_we0e6sW9IK_Xjrw1szQ"
CLIENT_SECRET = "6rDRP5Hfu6SykadFTDZ8BMi4zSQNUg"
PASSWORD = "CmhtIf!rc-6ZmoJ"
USER_AGENT = "Reed's politics scraper v1.0.0 (u/bewchacca-lacca)"
USERNAME = "bewchacca-lacca"

"""Create an instance for API access"""
reddit = asyncpraw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    password=PASSWORD,
    user_agent=USER_AGENT,
    username=USERNAME)

subreddit = await reddit.subreddit("neovim", fetch=True)

print("===================================")
print(subreddit.display_name)
print("===================================")
print(subreddit.title)
print("===================================")
print(subreddit.description)
