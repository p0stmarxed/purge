# PurgeScript

A script to reduce your follower count on Tumblr by softblocking some non-mutual followers.

## Dependencies

Dependencies:
* [requests-oauthlib](https://pypi.org/project/requests-oauthlib/)
* [ratelimit](https://pypi.org/project/ratelimit/)

## Authorization

This is a real pain.
1. Go [here](https://www.tumblr.com/oauth/apps) to "register" an app. The name, website & description can be anything, these values don't matter. For the default callback URL you can set, for example, `https://www.tumblr.com/dashboard`
2. Save your **OAuth Consumer Key** (used for `client_key`) and **Secret Key** (obtained by clicking "Show secret key" & used for `client_secret`).
3. Use these as parameters when running the script.

## Usage

Use it like this:
```shell
python purge.py -u <your_username> -m <max_followers_to_pull> -k <client_key> -s <client_secret>
```

**Note:** When you specify the max number of followers to pull, this is the number of recent followers that is checked, among which non-mutuals are blocked, NOT necessarily the number of users that will be blocked.