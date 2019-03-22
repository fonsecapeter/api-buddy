# Preferences
All the things that you don't want to type in every command can be set in your preferences. They live in `~/.api-buddy.yml` and should be writtend in [yaml format](https://yaml.org). There's currently only one you *have* to set (`api_url`), but there's plenty more to configure for a better API exploration experience.

At maximum a preferences configuration might look something like this:
```yaml
api_url: https://api.url.com
auth_type: oauth2
oauth2:
  client_id: your_client_id
  client_secret: your_client_secret
  scopes:
    - one_scope
    - another_scope
auth_test_status: 401
api_version: 2
verify_ssl: false
timeout: 100
headers:
  Cookie: flavor=chocolate-chip; milk=please;
  Origin: your-face
verboseness:
  request: true
  response: true
indent:
  4
theme: paraiso-dark
variables:
  user_id: ab12c3d
  email: me@email.com
```

But at minimum, you just need to specify this:
```yaml
api_url: https://some.url.com
```

## Configuration Reference
All the possible knobs you can dial are (with defaults shown if optional):

#### API URL
>`str` (required)
```yaml
api_url: https://base.api-url.com
```

This is your base API URL. It's' be the part of the url that comes before all the endpoints you want to hit. For example, if you wanted to hit `https://api.url.com/an-endpoint`, it would be `https://api.url.com`.


#### Auth Type
> `null` or `str` (optional)
```yaml
auth_type: null
```

This is the type of authentication you'll use. If you don't specify or use `null` it will default to no authentication, but oauth2 is also supported. [Read more about OAuth2 authentication here](/docs/oauth2.md). It's super easy, I promise 😬

You can also always manually set headers for authentication (more on that below).

#### Auth Test Status
> `int` (optional)
```yaml
auth_test_status: 401
```

This is status code that indicates it's time to reauthorize. You only need to specify this if you're using an auth type. If API Buddy encounters this status code after an API call, and you're using authentication, it'll re-authorize then try again. It really should be `401`, but not all APIs are designed the same. 😸

#### API Version
> `null`, `str`, `int`, or `float` (optional)
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

#### Timeout
> `int` (optional)
```yaml
timeout: 60
```

This is the time (in seconds) to wait for a request to respond. You can bump it up if you're getting timeout errors.

#### Headers
> `Dict[str, str]` (optional)

If you have any extra headers you want to send on every request, add them here. You can add them in simple yaml dictionary format, ex:
```yaml
headers:
  Authorize: basic ab1c23d4
  Something: else
```

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

You can [read more about this here](/docs/variables.md), but these are super handy for arbitrary things you want to interpolate throughout your commands.

#### Indent
> `int` or `null` (optional)
```yaml
indent: 2
```

You can change how many spaces your JSON formatting indents. If you don't want any expanded json at all, just set this to `null`.

#### Theme
> `str` or `null` (optional)
```yaml
theme: shellectric
```

You can change up the colors with different themes. Options are:
- abap
- algol
- algol_nu
- arduino
- autumn
- borland
- bw
- colorful
- default
- emacs
- friendly
- fruity
- igor
- lovelace
- manni
- monokai
- murphy
- native
- paraiso-dark
- paraiso-light
- pastie
- perldoc
- rainbow_dash
- rrt
- shellectric
- tango
- trac
- vim
- vs
- xcode
