import praw
import pytest
import logging

from discussion import parse_comment_content, parse_comments

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
    "DDD Weekly Nov10 9 calls",
    "AABA Dec 80 calls",
    "ATVI Dec 52.5 calls",
    "NRG Nov 27 puts",
    "Baba Jan 190s hit twice for $1.5m call sweeps",
    "Qqq 12/8 152 put sweep for $475k",
]

statement_results = [
    [dict(ticker="TSLA",    strike=330.0,   expiration="Jan",       option="call")],
    [dict(ticker="JD",      strike=40.0,    expiration="May",       option="call")],
    [
        dict(ticker="AMD", strike=12.0, expiration="Weekly", option="call"),
        dict(ticker="AMD", strike=12.5, expiration="Weekly", option="call"),
    ],
    [dict(ticker="DDD",     strike=9.0,     expiration="Weekly",    option="call")],
    [dict(ticker="AABA",    strike=80.0,    expiration="Dec",       option="call")],
    [dict(ticker="ATVI",    strike=62.5,    expiration="Weekly",    option="call")],
    [dict(ticker="NRG",     strike=27.0,    expiration="Nov",       option="put")],
    [dict(ticker="BABA",    strike=190.0,   expiration="Jan",       option="call")],
    [dict(ticker="QQQ",     strike=152.0,   expiration="12/8",      option="put")],
]

def check_statement_result(entry, expected_entry):
    for key in expected_entry:
        assert expected_entry[key] == entry[key]

@pytest.mark.parametrize("statement,expected_result", list(zip(statement_examples, statement_results)))
def test_statement_examples(statement, expected_result):
    result = list(parse_comment_content(statement))
    log.info(result)
    for (entry, expected_entry) in zip(result, expected_result):
        check_statement_result(entry, expected_entry)

def test_sample_discussion_parse_comments(sample_discussion):
    result = list(parse_comments(sample_discussion))
    log.info(result)