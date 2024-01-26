import asyncio
import asyncpraw

# credentials
CLIENT_ID = "gB_we0e6sW9IK_Xjrw1szQ"
CLIENT_SECRET = "6rDRP5Hfu6SykadFTDZ8BMi4zSQNUg"
PASSWORD = "CmhtIf!rc-6ZmoJ"
USER_AGENT = "Reed's politics scraper v1.0.0 (u/bewchacca-lacca)"
USERNAME = "bewchacca-lacca"

# search parameters
SEED_SUBREDDITS = ['Republican', 'democrats']

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
    """Get the top n submissions from the specified subreddit."""
    subreddit = await reddit.subreddit(subreddit)
    submissions = []
    async for submission in subreddit.top(time_filter=time_filter, limit=n_submissions):
        submissions.append(submission)
    return submissions

async def get_post_comments(post, reddit):
    """Get the comments on a single post. For use in a loop to hand multiple post."""
    post = await reddit.submission(post)
    comments = []
    async for comment in post.comments():
        comments.append(comment)
    return comments
        
async def main():

    # start reddit instance
    reddit = await setup_access()
    
    # pull in posts
    posts = await top_posts(subreddit='Republican', n_submissions=1,
                            time_filter='month', reddit=reddit)
    
    # for each post, get all comments and add them to a single list
    all_comments = [] 
    async for post in posts:
        post_comments = await get_post_comments(post=post, reddit=reddit)
        all_comments.append(post_comments)
    
    for post in posts:
        print(f'Post ID: {post}')
    
    await reddit.close()

if __name__ == "__main__":
    asyncio.run(main())