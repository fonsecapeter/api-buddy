# API Buddy

[![Build Status](https://travis-ci.org/fonsecapeter/api-buddy.svg?branch=master)](https://travis-ci.org/fonsecapeter/api-buddy.svg)

Explore APIs from your console with API Buddy

> Right now, only OAuth2 authentication is supported. It's the most common, and current gold standard for security best practices. Also most APIs use it. That said, I have no beef with all the APIs out there using something else, so feel free to open a ticket if you want something else supported. 🎟

## Usage

It's as easy as:
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

### Preferences
All the things that you don't want to type in every command can be set in your preferences. They live in `~/.api-buddy.yml` and should be writtend in [yaml format](https://yaml.org). There's currently only one you *have* to set (`api_url`), but there's plenty more to configure for a better API exploration experience.

The basic knobs you can dial are (with defaults shown):

#### API URL
>`str` (required)
```yaml
api_url: https://api.url.com
```

This is your base API URL. It's' be the part of the url that comes before all the endpoints you want to hit. For example, if you wanted to hit `https://api.url.com/an-endpoint`, it would be `https://api.url.com`.


#### Auth Type
> `null` or `str` (optional)
```yaml
auth_type: null
```

This is the type of authentication you'll use. If you don't specify or use `null` it will default to no authentication, but oauth2 is also supported. [Read more about authentication here](docs/authentication.md). It's super easy, I promise 😬

**TL;DR** OAuth2 is currently the only other supported option and looks like this:
```yaml
auth_type: oauth2
oauth2:
  client_id: your_client_id
  client_secret: your_client_secret
  scopes:
    - one_scope
    - another_scope
```

#### Auth Test Status
> `int` (optional)
```yaml
auth_test_status: 401
```

This is status code that indicates it's time to reauthorize. You only need to specify this if you're using an auth type. If API Buddy encounters this status code after an API call, and you're using authentication, it'll re-authorize then try again. It really should be `401`, but not all APIs are designed the same. 😸

#### API Version
> `null` or `str` (optional)
```yaml
api_version: null
```

If your API uses versioning, you can specify this and not have to type all the time. Not all APIs use this, but a lot of them do, so it's just a convenience -- is ignored if left out or `null`. Would be like this: `https://an.api.com/<version>/my-fav-endpoint`.

#### Verify SSL
> `bool` (optional)
```yaml
verify_ssl: true
```

By default, API Buddy will not allow you to communicate over http or though an untrusted SSL certificate. We're all adults here, if you want to override that just use this setting. It's something you'll probably want to do if you're actually developing the API you're exploring and it's running on localhost.

#### Verboseness
> `Dict[str, bool]` (optional)
```yaml
verboseness:
  request: false
  response: false
```

If you want to see more details about what you're doing, this is the place to do it. Just specify `true` on the one you want and you're good to go.

#### Variables
> `Dict[str, str]` (optional)
```yaml
variables: {}
```

You can [read more about this here](docs/variables.md), but these are super handy for arbitrary things you want to interpolate throughout your commands.


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
