# API Buddy
[![Build Status](https://circleci.com/gh/fonsecapeter/api-buddy.svg?style=svg)](https://circleci.com/gh/fonsecapeter/api-buddy)
[![PyPI version](https://badge.fury.io/py/api-buddy.svg)](https://badge.fury.io/py/api-buddy)

<img src="https://raw.githubusercontent.com/fonsecapeter/api-buddy/main/media/icon.png" alt="demo">

## Demo
<img src="https://raw.githubusercontent.com/fonsecapeter/api-buddy/main/media/demo.gif" alt="demo">

The most pleasant HTTP API CLI tool
- Quick to set up
- Easy to use
- Automated OAuth2 sign-in
- Copy/paste-able results

## Installation

As long as you have python 3.13 or higher (I recommend using [pyenv](https://github.com/pyenv/pyenv)), just:
```bash
pip install api-buddy
```

## Usage

First, specify the API you're exploring
```bash
api use https://some.api.com
```

Which will set the `api_url` value in your preferences file
```yaml
# ~/.api-buddy.yaml
api_url: https://some.api.com
```

Then it's as easy as:
```bash
api get some-endpoint
```
```javascript
=> 200
{
  "look": "I haz data",
  "thx": "API Buddy"
}
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

🤔 Note the single-quotes, which keeps your json as a sing continuous string.
This means you can expand across multiple lines too:
```bash
api post \
  some-endpoint \
  '{
     "id": 1,
     "field": "value"
  }'
```

Variables can be interpolated within your endpoint, as part
of values in your query params, or anywhere in your request
body data, as long as they're defined by name in your
preferences:
``` bash
api post \
  'users/#{{user_id}}' \
  'name=#{{name}}' \
  '{
    "occupation": "#{{occupation}}"
  }'
```

### [👉 See all the helpful preferences here](https://github.com/fonsecapeter/api-buddy/blob/master/docs/preferences.md)

### Arguments
- `use`: (optional) Set the base `api_url` you're exploring in your preferences file.
  - It come with  the actual `api_url` value

If you're actually sending an HTTP request:
- `http_method`: (optional) The HTTP method to use in your request.
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
- Python 3.13
  - Suggest using: [pyenv](https://github.com/pyenv/pyenv)

Steps to start working:
- Build and create the local venv with `bin/setup`
- Make sure everything works with `bin/test`
- Try the local cli with `poetry run api --help`
- Find other management commands with `bin/list`

Note to self, publish flow is:
- `bin/bump`
- `git commit -m 'Major/Minor/Patch bump x.x.x -> y.y.y'`
- `bin/publish`
- `git push`
- `bin/tag`
