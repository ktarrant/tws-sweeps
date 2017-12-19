import praw
from collections import OrderedDict
from datetime import date
import pandas as pd

from discussion import parse_comments

from credentials import CLIENT_ID, CLIENT_SECRET

discussion_ids = OrderedDict([
    (date(2017, 12, 18), "7kl4zv"),
    (date(2017, 12, 15), "7jzmdi"),
    (date(2017, 12, 14), "7jrh70"),
    (date(2017, 12, 13), "7jj34w"),
    (date(2017, 12, 12), "7jampt"),
    (date(2017, 12, 11), "7j244j"),
    (date(2017, 12,  8), "7ievp6"),
    (date(2017, 12,  7), "7i6d0m"),
    (date(2017, 12,  6), "7hxxjk"),
    (date(2017, 12,  5), "7hpkmv"),
    (date(2017, 12,  4), "7hh8mb"),
])

def _load_discussions(reddit):
    for dt in discussion_ids:
        discussion_id = discussion_ids[dt]
        submission = reddit.submission(id=discussion_id)
        yield parse_comments(submission)

if __name__ == "__main__":
    reddit = praw.Reddit(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        user_agent='tws-sweeps',
                        )

    output = pd.concat(list(_load_discussions(reddit)))
    print(output)
    output.to_csv("scratch.csv")