# Variables
If you find yourself typing a specific value a bunch of times, or just don't want to commit some 9-character hash to memory, you can save them in your preferences. The best part is, you'll be able to use them throughout your commands without having to type them out each time.

Let's say you're interacting with an API and want to keep track of your user's information. You can just define some variables in your preferences like this:
```yaml
variables:
  - user_id: 123
  - name: Art Vandalay
```

And now you can reference them like this:
```bash
api get '/users/#{user_id}'
```

API Buddy would interpolate the `user_id` variable and hit the `/users/123` endpoint.

You can use variables within in your endpoint, as part of values in your query params, or anywhere in your request body data.
```bash
api post '/users/' \
  'id=#{user_id}' \
  '{
    "id"=#{user_id},
    "name"="#{name}"
  }'
```
