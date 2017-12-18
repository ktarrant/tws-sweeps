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
    ("ticker", (r"[A-Z]{2,5}", ["ticker"])),
    ("expiration",  ("|".join(["{}(?:{})?".format(prefix, suffix) for prefix, suffix in month_options]),
                     ["expiration"])),
    ("strike", ((r"(c|p|C|P)?([1-9][0-9]{0,3})(c|p|C|P)?"), ["_num", "option_p", "num", "option_s"])),
    ("option", (r"call|put", ["option_e"])),
])
sweep_elements_re_keys = [key for element in sweep_elements for key in sweep_elements[element][1]]
sweep_elements_re = re.compile("|".join(["(" + sweep_elements[key][0] + ")" for key in sweep_elements]))

def _parse_comment_content(content):
    """
    :param content: str
    :yield: OrderedDict's each representing a statement in the comment
    """
    statements = re.split(r",|;|\(|\)|" + "\n", content)
    for statement in statements:
        log.debug("[Processing Statement] {}".format(statement))
        sweep_elements_matches = sweep_elements_re.findall(statement)

        combined_result = OrderedDict()
        for match in sweep_elements_matches:
            result = {key: value for key, value in zip(sweep_elements_re_keys, match)}
            for key in result:
                if result[key] != '':
                    combined_result[key] = result[key]

        if len(combined_result.keys()) > 0:
            yield combined_result

def parse_comments(submission):
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        for combined_result in _parse_comment_content(comment.body):
            if all([k in combined_result for k in ["ticker", "expiration", "num"]]):
                log.info("[Found Sweep] {}".format(combined_result))
                yield combined_result