import re
import logging
from collections import OrderedDict

log = logging.getLogger(__name__)

month_options = [
    ("Jan", "uary"),
    ("Feb", "ruary"),
    ("Mar", "ch"),
    ("Apr", "il"),
    ("May|Jun", "e"),
    ("Jul", "y"),
    ("Aug", "ust"),
    ("Sep", "tember"),
    ("Oct", "ober"),
    ("Nov|Dec", "ember"),
    ("Week|week", "ly|lies")
]
sweep_elements = OrderedDict([
    ("ticker", (r"(^[A-Z][A-Za-z]{1,3})|[A-Z]{0-4}", ["ticker", "_ticker"])),
    ("expiration",  ("|".join(["{}(?:{})?".format(prefix, suffix) for prefix, suffix in month_options]),
                     ["expiration"])),
    ("strike", ((r"(c|p|C|P)?([1-9][0-9]{0,3})(c|p|C|P)?"), ["_strike", "option_p", "strike", "option_s"])),
    ("option", (r"call|put", ["option_e"])),
])
sweep_elements_re_keys = [key for element in sweep_elements for key in sweep_elements[element][1]]
sweep_elements_re = re.compile("|".join(["(" + sweep_elements[key][0] + ")" for key in sweep_elements]))

def parse_comment_content(content):
    """
    Parse the given string for mentions of spreads. Yield any spreads
    :param content: str
    :yield: dict's each representing a statement in the comment
    """
    statements = re.split(r",|;|\(|\)|" + "\n", content)
    for statement in statements:
        log.debug("[Processing Statement] {}".format(statement))
        sweep_elements_matches = sweep_elements_re.findall(statement)

        entry = {}
        for match in sweep_elements_matches:
            for re_key, value in zip(sweep_elements_re_keys, match):
                if re_key.startswith("_") or value == "":
                    continue

                s_key = re_key.split("_")[0]
                if s_key in entry:
                    log.error("Throwing away match: ({key}, {value})".format(key=s_key, value=value))
                else:
                    if s_key == "strike":
                        entry[s_key] = float(value)
                    elif s_key == "option":
                        if value.lower().startswith("c"):
                            entry[s_key] = "call"
                        elif value.lower().startswith("p"):
                            entry[s_key] = "put"
                        else:
                            log.error("Invalid option type matched: {}".format(value))
                    elif s_key == "expiration":
                        if value.lower().startswith("week"):
                            entry[s_key] = "Weekly"
                        else:
                            entry[s_key] = value
                    else:
                        entry[s_key] = value

        yield entry


def parse_comments(submission):
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        for combined_result in parse_comment_content(comment.body):
            if all([k in combined_result for k in ["ticker", "expiration", "num"]]):
                log.info("[Found Sweep] {}".format(combined_result))
                yield combined_result