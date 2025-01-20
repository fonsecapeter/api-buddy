from docopt import docopt

from api_buddy.utils.typing import Options
from api_buddy.validation.options import validate_options


def load_options(doc: str) -> Options:
    opts = docopt(doc)
    return validate_options(opts)
