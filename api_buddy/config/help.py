from colorama import Fore, Style

BRIGHT_GREEN = f'{Style.BRIGHT}{Fore.GREEN}'
BRIGHT_NORMAL = f'{Style.RESET_ALL}{Style.BRIGHT}'
API_CLI = f'{BRIGHT_GREEN}api{BRIGHT_NORMAL}'
BACKSLASH = f'{Fore.MAGENTA}\\'

HELP = f"""\nExplore OAuth2 APIs from your console with API Buddy

It's as easy as:
{API_CLI} get some-endpoint{Style.RESET_ALL}

HTTP Method defaults to get:
{API_CLI} this-endpoint{Style.RESET_ALL}

You can add query params in key=val format:
{API_CLI} get {BACKSLASH}
  {BRIGHT_NORMAL}my/favorite/endpoint {BACKSLASH}
  {BRIGHT_NORMAL}first_name=cosmo {BACKSLASH}
  {BRIGHT_NORMAL}last_name=kramer{Style.RESET_ALL}

You can also add request body data in JSON format:
{API_CLI} post {BACKSLASH}
  {BRIGHT_NORMAL}some-endpoint {BACKSLASH}
  {Fore.RED}'{{"id": 1, "field": "value"}}'{Style.RESET_ALL}

Note the single-quotes, you can also expand this accross
multiple lines:
{API_CLI} post {BACKSLASH}
  {BRIGHT_NORMAL}some-endpoint {BACKSLASH}
  {Fore.RED}'{{
     "id": 1,
     "field": "value"
  }}'{Style.RESET_ALL}

Variables can be interpolated within your endpoint, as part
of values in your query params, or anywhere in your request
body data, as long as they're defined by name in your
preferences:
{API_CLI} post {BACKSLASH}
  {BRIGHT_NORMAL}users/#{{user_id}} {BACKSLASH}
  {BRIGHT_NORMAL}name=#{{name}} {BACKSLASH}
  {Fore.RED}'{{
    "occupation"="#{{occupation}}"
  }}'{Style.RESET_ALL}

Your preferences live in {Fore.MAGENTA}~/.api-buddy.yml{Style.RESET_ALL}
Check out GitHub for more info
{Fore.BLUE}{Style.BRIGHT}https://github.com/fonsecapeter/api-buddy{Style.RESET_ALL}

Arguments:
  http_method  (optional, default: get) One of
                 [get, post, patch, put, delete]
  endpoint     The relative path to an API endpoint
  params       (optional) A list of key=val query params
  data         (optional) A JSON string of request body
                 data, for all methods but 'get'

Usage:
  api help
  api (-h | --help)
  api (-v | --version)
  api get <endpoint> [<params> ...]
  api post <endpoint> [<params> ...] [<data>]
  api patch <endpoint> [<params> ...] [<data>]
  api put <endpoint> [<params> ...] [<data>]
  api delete <endpoint> [<params> ...] [<data>]
  api <endpoint> [<params> ...]

Options:
  -h, --help     Show this help message
  -v, --version  Show installed version
"""
