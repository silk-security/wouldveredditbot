import os
import praw
import praw.models
from praw.exceptions import PRAWException
from prawcore.exceptions import PrawcoreException
import re
import backoff
from dotenv import load_dotenv
import pickle

load_dotenv()

SECRET = os.environ.get("SECRET")
CLIENT_ID = os.environ.get("CLIENT_ID")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")




def handler(details):
    wait = details['wait']
    print(f"Backing off for {wait:0.1f} seconds")

@backoff.on_exception(wait_gen=backoff.expo,exception=[PRAWException, PrawcoreException], max_tries=5,on_backoff=handler)
def read_sub_comments(subreddit: praw.models.Subreddit):
    for comment in subreddit.stream.comments():
        if comment in seen_comments:
            continue
        elif comment.author is not None and comment.author.name != reddit.user.me().name:
            if regex_match := re.search(r"(would|could|should) of", comment.body):
                print(f"Found {regex_match[1]}")
                # comment.reply(f'Hi! I just wanted to let you know that you said "{regex_match[1]} of" when the correct spelling is "{regex_match[1]}\'ve" which is actually a contraction of "{regex_match[1]} have." Hope this helps!\n\n_I am a bot, and this action was performed automatically._')
        
        seen_comments.add(comment.id)

if __name__ == '__main__':
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=SECRET,
        user_agent='wouldvebot by u/thefantasticphantasm',
        username=USERNAME,
        password=PASSWORD
    )

    subreddit = reddit.subreddit("test")

    try:
        with open("comments.pk", 'rb') as f:
            seen_comments = pickle.load(f)
    except Exception:
        seen_comments = set()

    subreddit_strs = ["test"]
    subreddits = [reddit.subreddit(sub) for sub in subreddit_strs]

    try:
        for sub in subreddits:
            read_sub_comments(sub)
    finally:
        with open("comments.pk", 'wb') as f:
            pickle.dump(seen_comments, f)

