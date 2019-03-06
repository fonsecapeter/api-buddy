# API CLI Buddy

[![Build Status](https://travis-ci.org/fonsecapeter/api-buddy.svg?branch=master)](https://travis-ci.org/fonsecapeter/api-buddy.svg)

Explore APIs from your console with API Buddy

> Right now, only OAuth2 authentication is supported. It's the most common, and current gold standard for good security practices. Also most APIs use it. That said, I have no beef with all the APIs out there using something else, so feel free to open a ticket if you want something else supported. 🎟

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
All the things that you don't want to type in every cli command live in your preferences. These will be where you keep track of what API you're messing around with, your OAuth2 credentials, and general API Buddy configuration.

They live in `~/.api-buddy.yml` and should look something like this:
```yaml
api_url: https://base.api.url.com
client_id: your_client_id
client_secret: your_client_secret
scopes:
  - one_scope
  - another_scope
```

In case you didn't know that's [yaml format](https://yaml.org).

You'll have to specify these (with examples shown):
```yaml
api_url: https://base.api.url.com
  # (str) The base api url you'll be using
client_id: your_client_id
  # (str) Part of your api provider dev account
client_secret: your_client_secret
  # (str) Part of your api provider dev account
  #       (PROTECT THIS, IT'S SECRET) 🙊
scopes:
  - one_scope
  - another_scope
  # (List[str]) Specify which resources you want to
  #             access
```

And can optionally specify these (with defaults shown):
```yaml
redirect_uri: http://localhost:8080/
  # (str) Part of your api provider dev account, needs to
  #       be on localhost
auth_fail_path: 401
  # (int) Response status code that means you need to
  #       re-authorize
api_version: null
  # (str) If your api uses versioning, you can specify
  #       this and not have to type it all the time.
  #       https://an.api.com/<version>/my-fav-endpoint
variables:
  my_var: some value
  another_var: some other value
  # (Dict[str, str]) Specify variables for use throughout
  #                  your options, see ##Advanced Usage for
  #                  more info
```

### Arguments
- `http_method`: (Optoinal, default: `get`) The HTTP method to use in your request.
  - It should be one of `get`, `post`, `patch`, `put`, `delete`.
- `endpoint`: The relative path to an API endpoint.
  - AKA you don't need to type the base api url again here.
- `params`: (optional) A list of `key=val` query params
- `data`: (optional) A JSON string of requets body data.
  - You can't use this with `get` because HTTP.


### Options
- `-h`, `--help`: Show the help message
- `-v`, `--version`: Show the installed version

## Advanced Usage
### Variables
If you find yourself typing a specific value a bunch of times, like a user id or something, you can put arbitrary variables into your preferences and they'll be interpolated throughout your arguments if you wrap them in `#{}`. For example, if you had this in your preferences:
```yaml
# in preferences
variables:
  - user_id: 123
  - name: Art Vandalay
```

You could do this:
```bash
api get '/users/#{user_id}'
```

And API Buddy would hit the `/users/123` endpoint.

You can also use variables as values in your query params, or anywhere in your request body data.
```bash
api post '/users/' \
  'id=#{user_id}' \
  '{
    "id"=#{user_id},
    "name"="#{name}"
  }'
```

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
