# API Buddy

[![Build Status](https://travis-ci.org/fonsecapeter/api-buddy.svg?branch=master)](https://travis-ci.org/fonsecapeter/api-buddy.svg)
[![PyPI version](https://badge.fury.io/py/api-buddy.svg)](https://badge.fury.io/py/api-buddy)

![Demo](/media/demo.gif 'demo.gif')

> Right now, only OAuth2 authentication is supported. It's the most common, and current gold standard for security best practices. Also most APIs use it. That said, I have no beef with all the APIs out there using something else, so feel free to open a ticket if you want something else supported. 🎟
>
> You can also always manually set headers.

## Installation

As long as you have python 3.7 or higher (I recommend using [pyenv](https://github.com/pyenv/pyenv)), just:
```bash
pip install api-buddy
```

## Usage

First, specify the API you're exploring in your preferences
```yaml
# ~/.api-buddy.yaml
api_url: https://some.api.com
```

Then it's as easy as:
```bash
api get some-endpoint
```
```json
=> 200
{
  "look": "I haz data",
  "thx": "API Buddy"
}
```

HTTP Method defaults to `get`:
```bash
api this-endpoint  # same as first example
```

You can add query params in key=val format:
```bash
api get \
  my/favorite/endpoint \
  first_name=cosmo \
  last_name=kramer
```

You can also add request body data in JSON format:
```bash
api post \
  some-endpoint \
  '{"id": 1, "field": "value"}'
```

🤔 Note the single-quotes. You can expand this accross multiple lines:
```bash
api post \
  some-endpoint \
  '{
     "id": 1,
     "field": "value"
  }'
```

### [Preferences 👉](https://github.com/fonsecapeter/api-buddy/blob/master/docs/preferences.md)

### Arguments
- `http_method`: (optional, default=`get`) The HTTP method to use in your request.
  - It should be one of:
    - `get`
    - `post`
    - `patch`
    - `put`
    - `delete`
- `endpoint`: (required) The relative path to an API endpoint.
  - AKA you don't need to type the base api url again here.
- `params`: (optional) A list of `key=val` query params
- `data`: (optional) A JSON string of requets body data.
  - You can't use this with `get` because HTTP.


### Options
- `-h`, `--help`: Show the help message
- `-v`, `--version`: Show the installed version

## Development
Requires:
- [poetry](https://poetry.eustace.io/)
- Python 3.7
  - Suggest using: [pyenv](https://github.com/pyenv/pyenv)

Steps to start working:
- Build and create the local venv with `bin/setup`
- Make sure everything works with `bin/test`
- Try the local cli with `poetry run api --help`
- Find other management commands with `bin/list`
