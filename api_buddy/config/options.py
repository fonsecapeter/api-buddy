from docopt import docopt
from ..typing import Options


def load_options(doc: str) -> Options:
    opts: Options = docopt(doc)
    return opts
