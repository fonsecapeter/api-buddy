from typing import cast

from colorama import init as init_colorama

from api_buddy.config.help import HELP
from api_buddy.config.options import load_options
from api_buddy.config.preferences import load_prefs, save_api_url
from api_buddy.config.variables import interpolate_variables
from api_buddy.network.request import send_request
from api_buddy.network.response import print_response
from api_buddy.network.session import get_session
from api_buddy.utils import PREFS_FILE, VERSION
from api_buddy.utils.exceptions import APIBuddyException, exit_with_exception


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
