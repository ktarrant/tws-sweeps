import praw
import re

from credentials import CLIENT_ID, CLIENT_SECRET

def get_instance():
    return praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    user_agent='tws-sweeps',
                    )

ticker_re = re.compile(r"[A-Z]{2,5}")

if __name__ == "__main__":
    reddit = get_instance()

    # https://www.reddit.com/r/thewallstreet/comments/
    discussion_id = "7bd2dw"

    submission = reddit.submission(id=discussion_id)

    submission.comments.replace_more()
    for top_level_comment in submission.comments:
        content = top_level_comment.body
        tickers = ticker_re.findall(content)
        print(tickers)