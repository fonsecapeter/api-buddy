from copy import deepcopy
from typing import cast, Dict, Union
from urllib.parse import urlparse
from ..typing import Options
from ..exceptions import APIBuddyException


def _validate_endpoint(endpoint: Union[str, bool]) -> str:
    valid_endpoint = str(endpoint)
    url_parts = urlparse(valid_endpoint)
    if url_parts.scheme:
        raise APIBuddyException(
            title='Check your endpoint, dude',
            message=(
                'You don\'t need to supply the full url, just the path.\n'
                f'Did you mean "{url_parts.path}"?'
            )
        )
    return valid_endpoint


def validate_options(opts: Dict['str', Union[str, bool]]) -> Options:
    """Convert types and validate"""
    valid_opts = deepcopy(opts)
    valid_opts['<endpoint>'] = _validate_endpoint(opts['<endpoint>'])
    valid_opts['get'] = True  # TODO only do this if not using a different method
    return cast(Options, valid_opts)
