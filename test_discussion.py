import praw
import pytest
import logging

from discussion import _parse_comment_content, parse_comments

from credentials import CLIENT_ID, CLIENT_SECRET

log = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def reddit_instance(request):
    return praw.Reddit(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    user_agent='tws-sweeps',
                    )

@pytest.fixture
def sample_discussion(reddit_instance):
    # https://www.reddit.com/r/thewallstreet/comments/
    discussion_id = "7bd2dw"

    submission = reddit_instance.submission(id=discussion_id)

    return submission

statement_examples = [
    "TSLA Jan C330 buyer 1k contracts 10.85-11.05 for ~$1.1mm prem",
    "JD May C40 buyer of 580 contracts @4.",
    "AMD weekly C12 & C12.5 going.",
    "20k contracts Jan C12/C13 spread went off",
    "ATVI $62.5C and $65C have lots of volume as well",
    "DDD Weekly Nov10 9 calls",
    "AABA Dec 80 calls",
    "ATVI Dec 52.5 calls",
    "NRG Nov 27 puts",
    "edit: what a joke. 5k contracts Nov C20 swept this morning at .3",
    "Baba Jan 190s hit twice for $1.5m call sweeps",
    "Qqq 12/8 152 put sweep for $475k",
]

@pytest.mark.parametrize("statement", statement_examples)
def test_statement_examples(statement):
    result = list(_parse_comment_content(statement))
    log.info(result)

def test_sample_discussion_parse_comments(sample_discussion):
    result = list(parse_comments(sample_discussion))
    log.info(result)