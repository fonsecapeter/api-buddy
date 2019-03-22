from json import loads, JSONDecodeError
from copy import deepcopy
from colorama import Fore, Style
from typing import Any, cast, List
from urllib.parse import urlparse
from ..utils.typing import Options, RawOptions
from ..utils.exceptions import APIBuddyException
from ..utils.http import HTTP_METHODS, GET, pack_query_params


def _more_than_one_method_selected(opts: RawOptions) -> bool:
    return sum(
        cast(bool, opts[method]) for method in HTTP_METHODS
    ) > 1


def _validate_method(opts: RawOptions) -> RawOptions:
    """Converts named bools to str enum

    Implicitly removed the old docopt booleans from opts
    Defaults to 'get'
    """
    if _more_than_one_method_selected(opts):
        raise APIBuddyException(
            title='These HTTP methods are borked',
            message=(
                'It appears you selected more than one method...\n'
                'How did you even do this?'
            )
        )
    selected_method = GET
    for method in HTTP_METHODS:
        using_this_method = opts[method]
        del opts[method]
        if using_this_method is True:
            selected_method = method
    opts['<method>'] = selected_method
    return opts


def _validate_endpoint(endpoint: str) -> str:
    url_parts = urlparse(endpoint)
    if url_parts.scheme:
        message = 'You don\'t need to supply the full url, just the path.'
        path = url_parts.path
        if path:
            message += (
                f'\nDid you mean {Fore.BLUE}{Style.BRIGHT}{url_parts.path}'
                f'{Style.RESET_ALL}?'
            )
        raise APIBuddyException(
            title='Check your endpoint, dude',
            message=message,
        )
    return endpoint


def _validate_data(data: str) -> Any:
    try:
        return loads(data)
    except JSONDecodeError:
        raise APIBuddyException(
            title='Your request body data are wack',
            message=(
                'Please use valid json for: '
                f'{Fore.MAGENTA}{data}{Style.RESET_ALL}'
            ),
        )


def _validate_params_and_data(opts: RawOptions) -> RawOptions:
    """Validate query params and request body data

    Because of the cli argument signature, docopt always puts <data> at the end
    the <params> if it's given, and None in opts['<data>'] no matter what. It
    can't ever know the difference between the last param and the optional data
    arg, so we have to check the last param and see if it's data.
    """
    params = cast(List[str], opts['<params>'])
    data = None
    if len(params) > 0:
        maybe_data = params[-1]
        maybe_params = params[:-1]
        try:
            data = _validate_data(maybe_data)
        except APIBuddyException as data_err:
            try:  # maybe it's a param?
                pack_query_params([maybe_data])
            except APIBuddyException:
                if opts['<method>'] != GET:  # should never be data for GET
                    raise data_err  # it's not a param, its bad data
        else:  # maybe_data is data
            params = maybe_params
    if data is not None and opts['<method>'] == GET:
        raise APIBuddyException(
            title=(
                'You can\'t use request body data with '
                f'{Fore.MAGENTA}GET{Style.RESET_ALL}'
            ),
            message=(
                'Did you mean to use '
                f'{Fore.MAGENTA}POST{Style.RESET_ALL}?'
            ),
        )
    opts['<params>'] = pack_query_params(params)  # type: ignore
    opts['<data>'] = data
    return opts


def _validate_help(opts: RawOptions) -> RawOptions:
    opts['--help'] = opts['help']
    del opts['help']
    return opts


def validate_options(opts: RawOptions) -> Options:
    """Convert types and validate"""
    valid_opts = deepcopy(opts)
    valid_opts['<endpoint>'] = _validate_endpoint(
        cast(str, valid_opts['<endpoint>'])
    )
    _validate_method(valid_opts)
    _validate_params_and_data(valid_opts)
    _validate_help(valid_opts)
    return cast(Options, valid_opts)
