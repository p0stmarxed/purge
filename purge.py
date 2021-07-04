#!/bin/env python

# import libraries
import sys, getopt
import webbrowser
import json

import requests
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1

# import this library to set rate limit	
from ratelimit import limits

# global vars - to avoid having a billion params everywhere
username = ''
max_to_block = 0
client_key = ''
client_secret = ''
resource_owner_key = ''
resource_owner_secret = ''
non_mutuals = []

# useful urls
base_url = 'http://api.tumblr.com/v2/blog/' + username + '.tumblr.com/'
blocks = base_url + 'blocks'
followers_url = base_url + 'followers'

# authorize
def authorize():
    request_token_url = 'https://www.tumblr.com/oauth/request_token'
    base_authorization_url = 'https://www.tumblr.com/oauth/authorize'

    oauth = OAuth1Session(client_key, client_secret=client_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)

    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    authorization_url = oauth.authorization_url(base_authorization_url)
    webbrowser.open(authorization_url)

    redirect_response = input('Paste the full redirect URL here: ')
    oauth_response = oauth.parse_authorization_response(redirect_response)

    verifier = oauth_response.get('oauth_verifier')

    access_token_url = 'https://www.tumblr.com/oauth/access_token'
    oauth = OAuth1Session(client_key,
        client_secret=client_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier)

def add_followers(followers, offset, limit):
    followers_to_add = requests.get(followers_url, params = {"offset": offset}, auth = queryoauth)
    followers_to_add = json.loads(followers_to_add.text)
    followers_to_add = followers_to_add['response']['users']
    followers.extend(followers_to_add)

# after the following function is run, followers should contain a list of dictionaries
# each dictionary item is a follower
# we can only get about 20 followers at a time though
# so to block more people we will need to create additional lists
# using the offset parameter we can make a GET request starting at the 20th follower
# then the 40th, 60th, etc. and then we can append those lists to the first follower list
def build_followers_list(queryoauth):
    followers = requests.get(followers_url, auth=queryoauth)
    followers = json.loads(followers.text)
    followers = followers['response']['users']

    followers = []
    range_max = int(max_to_block // 20)
    last_request_limit = 0

    if range_max * 20 < max_to_block:
        range_max += 1
        last_request_limit = range_max * 20 - max_to_block

    for i in range(1, range_max):
        print(i * 20)
        offset = i * 20
        limit = 20

        if i == range_max:
            limit = last_request_limit

        add_followers(followers, offset, limit)
    
    # create a new list that does not contain any mutuals
    global non_mutuals
    non_mutuals = [i for i in followers if not (i['following'] == True)]

# define a function that will be used to softblock every follower in non_mutuals		
def softblock(x):
    block = requests.post(blocks, data=x, auth=queryoauth)
    unblock = requests.delete(blocks, data=x, auth=queryoauth)
    if block.status_code == 201 and unblock.status_code == 200:
        return 'success'
    else:
        return 'failed'

@limits(calls=1, period=1)
def purge():
    for i in range(len(non_mutuals)):
        blog = {'blocked_tumblelog': non_mutuals[i]['name']}
        print(blog)
        softblock(blog)

# define a function that will be used to softblock every follower in non_mutuals
# tumblr api block and unblock calls are rate limited at 60 requests per minute
# decorator sets limit of 1 call per second, equivalent to 60 calls per minute
# purge() function will iterate through each item in the list, declare a variable containing the parameters needed for the block and unblock calls
# then call softblock() function
def purge():
    # query signing & call build followers list function
    queryoauth = OAuth1(client_key, client_secret,
                    resource_owner_key, resource_owner_secret,
                    signature_type='query')

    build_followers_list(queryoauth)

def main():
    long_args = ["help", "username=", "key=", "secret=", "max="]
    global username, max_to_block, client_key, client_secret

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:m:k:s:", long_args)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    
    for o, a in opts:
        if o in ("-u", "--username"):
            username = a
        elif o in ("-m", "--max"):
            max_to_block = int(a)
            if not isinstance(max_to_block, int):
                print("max to block must be an integer")
                sys.exit(2)
        elif o in ("-k", "--key"):
            client_key = a
        elif o in ("-s", "--secret"):
            client_secret = a
        else:
            assert False, "unhandled option"

    if not username or not max_to_block:
        print("username and max followers to block required")
        sys.exit(1)
    if not client_key or not client_secret:
        print("client key and secret required")
        sys.exit(1)

    authorize()
    purge()

if __name__ == "__main__":
    main()