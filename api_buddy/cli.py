from typing import cast
from colorama import init as init_colorama
from .config.help import HELP
from .config.options import load_options
from .config.preferences import load_prefs, save_api_url
from .config.variables import interpolate_variables
from .network.request import send_request
from .network.response import print_response
from .network.session import get_session
from .utils import VERSION, PREFS_FILE
from .utils.exceptions import APIBuddyException, exit_with_exception


def run() -> None:
    init_colorama()
    try:
        opts = load_options(HELP)
        if opts["--version"]:
            print(VERSION)
            return
        if opts["--help"]:
            print(HELP)
            return
        prefs = load_prefs(PREFS_FILE)
        if opts["<cmd>"] == "use":
            save_api_url(cast(str, opts["<api_url>"]), prefs, PREFS_FILE)
            return
        interpolated_opts = interpolate_variables(opts, prefs)
        sesh = get_session(interpolated_opts, prefs, PREFS_FILE)
        resp = send_request(sesh, prefs, interpolated_opts, PREFS_FILE)
        print_response(resp, prefs)
    except APIBuddyException as err:
        exit_with_exception(err)


if __name__ == "__main__":
    run()
