# OAuth2 authentication

Using [OAuth2](https://oauth.net/2/) is super easy. All you have to do is add a few things to your preferences file, and API Buddy will authenticate and re-authenticate as needed. You just need to make sure your `auth_type` is `oauth2` and then fill in the rest of your preferences under `oauth2`.

## Authorizing

As long as you have your prefernces set up, API Buddy will walk you through the oauth flow as needed. First, it'll attempt to make your API call (using the token from your preferences if there is one). If this returns a `401` status response (or whatever you have configured in `auth_test_status`), you'll pop over to your web browser.

There you'll sign into your test account (note this doesn't necessarily have to be the developer account, but usally can be). You'll then see the API provider's data sharing agreement (DSA) and be able to grant API Buddy access to your data.

After that, the API Provider will redirect you to your `redirect_uri`, which should look like an error since it won't actually be a real website. 😮

![Redirect URI](/media/redirect_uri.png 'redirect_uri.png')

But fear not! This is what it should be doing. You'll just copy that whole url and go back to your terminal where API Buddy will be waiting for you to paste it.

![Receive Code](/media/receive_code.png 'receive_code.png')

From there, API Buddy will re-do the request and give you the new response. 🎉


## Setting up your Preferences

At minimun, this is all you need to say:

```yaml
api_url: https://some.api.com
auth_type: oauth2
oauth2:
  client_id: your_client_id
  client_secret: your_client_secret
  scopes:
    - one_scope
    - another_scope
```

At maximum, you can specify all of these:
```yaml
api_url: https://some.api.com
auth_type: oauth2
oauth2:
  client_id: your_client_id
  client_secret: your_client_secret
  scopes:
    - one_scope
    - another_scope
  access_token: some_token_value
  token_path: token
  authorize_path: authorize
  redirect_uri: https://localhost:8080/
  authorize_params:
    - select_profile=true
    - some_other_param=a_value
```

### OAuth2 Preferences
Here are the OAuth2-specific preferences you can configure (with defaults shown if optional):

#### Client ID
> `str` (required)
```yaml
  client_id: abcd1234
```

This is the unique identifier of your API client. The API provider you're exploring should give this to you and it should be easy to find in some kind of developer dashboard.

#### Client Secret
> `str` (required)
```yaml
  client_secret: 5678efgh
```

**Don't share this value with anyone!** 🙊

This is the secret key that you have to use to get oauth tokens. It proves that you are who you say you are and should be right next to your `client_id` your API provider's developer dashboard.

#### Scopes
> `List[str]` (required)
```yaml
  scopes:
    - email
    - favorite_color
```

Scopes represent the specific pieces of data you'll be asking for. It's up to the API provider to implement these, but however they do, you'll need to just give some information about scopes you want your oauth token to grant access to.

#### Redirect URI
> `str` (optional)
```yaml
  redirect_uri: http://localhost:8080/
```

This is where you'll get redirected after agreeing to the DSA. It should be configured in your API provider's developer dashboard and will default to `http://localhost:8080/`.

> Note, API Buddy won't actually listen to this port, it just generally needs to:
  1. Match in your API provider's developer dashboard
    - You can change here, there or both
  2. Not be a real url so you can copy/paste the resulting url when your browser tries to go there after the DSA

#### Access Token
> `str` (optional)
```yaml
  access_token: can_haz_token
```

This is the actual oauth token that'll get added to your requests. It's here mostly so that you can see what it is if you need to use it somewher else (ex in some project you're developing). It's also hepful to be able to change or remove it if you want to force a re-authorization.

#### Authorize Path
> `str` (optional)
```yaml
  token_path: authorize
```

The authorize path is the relative path (from your base `api_url`) that you'll open in your browser to sign in and agree to the DSA, then generate an oauth code. It's usually just `authorize`, but in case your API uses something different, you can specify here.

> Note it's not a full, absolute url, but feel free to file a ticket if you really need it to be. 🎟

#### Token Path
> `str` (optional)
```yaml
  token_path: token
```

The token path is the relative path (from your base `api_url`) that you'll hit to exchange an oauth code for a token. It's usually just `token`, but in case your API uses something different, you can specify here.

> Note it's not a full, absolute url, but feel free to file a ticket if you really need it to be. 🎟

#### Authorize Params
> `List[str]` (optional)
```yaml
  authorize_params: []
```

Some APIs give you the option of changing the DSA and/or token behavior through extra query params at the authorize step. This just let's you specify them here if you need to. These should be specified just like param cli arguments.
