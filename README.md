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
python purgescript.py [--nice] -u <your_username> -m <number_to_block> -k <client_key> -s <client_secret>
```

All parameters are required except the `--nice` flag.

### `--nice`

If set, the purge script will exclude users that have sent an ask asking not to be purged *that has been tagged with #spare.* Ask needs to be non-anonymous and sent originally to the blog doing the purging. Up to `<number_to_block>` asks are looked at.

### `-u` (`--username`)

The user whose followers we're purging.

### `-m` (`--max`)

The number of followers to block. Mutuals will be excluded. If `--nice` flag is set, people who have sent *published* asks asking not to be purged will also be excluded.

### `-k` (`--key`)

Client key. See [Authorization](#Authorization) section.

### `-s` (`--secret`)

Client secret. See [Authorization](#Authorization) section.