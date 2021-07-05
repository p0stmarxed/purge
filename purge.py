#!/bin/env python

# import libraries
import json
from ratelimit import limits

# global vars
non_mutuals = []

# useful urls
base_url = 'http://api.tumblr.com/v2/blog/' + username + '.tumblr.com/'
blocks = base_url + 'blocks'
followers_url = base_url + 'followers'

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
    range_max = int(max_followers_to_consider // 20)
    last_request_limit = 0

    if range_max * 20 < max_followers_to_consider:
        range_max += 1
        last_request_limit = range_max * 20 - max_followers_to_consider

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
        return True
    else:
        return False

# define a function that will be used to softblock every follower in non_mutuals
# tumblr api block and unblock calls are rate limited at 60 requests per minute
# decorator sets limit of 1 call per second, equivalent to 60 calls per minute
# purge() function will iterate through each item in the list, declare a variable containing the parameters needed for the block and unblock calls
# then call softblock() function
@limits(calls=1, period=1)
def purge(queryoauth):
    build_followers_list(queryoauth)

    for i in range(len(non_mutuals)):
        blog = {'blocked_tumblelog': non_mutuals[i]['name']}
        print(blog)
        result = softblock(blog)

        if not result:
            print("Something went wrong with softblocking user ", blog)