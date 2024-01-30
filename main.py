import asyncio
import asyncpraw
import json

# credentials
CLIENT_ID = "gB_we0e6sW9IK_Xjrw1szQ"
CLIENT_SECRET = "6rDRP5Hfu6SykadFTDZ8BMi4zSQNUg"
PASSWORD = "CmhtIf!rc-6ZmoJ"
USER_AGENT = "Reed's politics scraper v1.0.0 (u/bewchacca-lacca)"
USERNAME = "bewchacca-lacca"

# search parameters
seeds_dict = json.load(open('seed-subreddits.json'))
SEED_SUBREDDITS = seeds_dict['all']

async def setup_access():
    """Create an instance for API access"""
    instance = asyncpraw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=PASSWORD,
        user_agent=USER_AGENT,
        username=USERNAME)
    return instance

async def top_posts(subreddit, n_submissions, time_filter, reddit):
    """Get the top n submissions from the specified subreddit.
    """
    subreddit = await reddit.subreddit(subreddit)
    submissions = []
    async for submission in subreddit.top(time_filter=time_filter, limit=n_submissions):
        submissions.append(submission)
    return submissions

async def get_post_comments(post, reddit):
    """Get the comments on a single post. To be used in a loop to handle multiple post.
    """
    post = await reddit.submission(post)
    comments = []
    async for comment in post.comments():
        comments.append(comment)
    return comments
        
async def main():

    # start reddit instance
    reddit = await setup_access()
    
    # pull in posts
    all_posts = []
    for sub in SEED_SUBREDDITS:
        posts = await top_posts(subreddit=sub, n_submissions=30, time_filter='year', reddit=reddit)
        all_posts.append(posts)
    
    # for each post, get all comments and add them to a single list
    all_comments = [] 
    async for post in all_posts:
        post_comments = await get_post_comments(post=post, reddit=reddit)
        all_comments.append(post_comments)
    
    await reddit.close()

if __name__ == "__main__":
    asyncio.run(main())