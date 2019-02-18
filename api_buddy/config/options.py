from docopt import docopt
from ..typing import Options
from ..validation.options import validate_options


def load_options(doc: str) -> Options:
    opts = docopt(doc)
    return validate_options(opts)
