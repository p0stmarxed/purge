# purge

# import libraries
import requests
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1

# authenticate
client_key = 'enter client key here'
client_secret = 'enter client secret here'

# enter the oauth token and secret you received from the authorize script
oauth_tokens = {'oauth_token': 'enter oauth token here', 'oauth_token_secret': 'enter oauth token secret here'}

# set oauth credentials to these variables for query signing
resource_owner_key = oauth_tokens.get('oauth_token')
resource_owner_secret = oauth_tokens.get('oauth_token_secret')

# set uri for blocking
blocks = 'http://api.tumblr.com/v2/blog/yoururl.tumblr.com/blocks'

# query signing
queryoauth = OAuth1(client_key, client_secret,
                    resource_owner_key, resource_owner_secret,
                    signature_type='query')

# set uri for retrieving list of your followers
followers_url = 'http://api.tumblr.com/v2/blog/yoururl.tumblr.com/followers'

# returns a JSON object containing your followers
followers = requests.get(followers_url, auth=queryoauth)

# convert JSON object to a standard python list
import json
followers = json.loads(followers.text)

# remove metadata at the top of the list
followers = followers['response']['users']

# followers should now contain a list of dictionaries
# each dictionary item is a follower
# we can only get about 20 followers at a time though
# so to block more people we will need to create additional lists
# using the offset parameter we can make a GET request starting at the 20th follower
# then the 40th, 60th, etc. and then we can append those lists to the first follower list

followers2 = requests.get(followers_url, params = {"offset": 20}, auth = queryoauth)
followers2 = json.loads(followers2.text)
followers2 = followers2['response']['users']
followers.extend(followers2)

followers3 = requests.get(followers_url, params = {"offset": 40}, auth = queryoauth)
followers3 = json.loads(followers3.text)
followers3 = followers3['response']['users']
followers.extend(followers3)

followers4 = requests.get(followers_url, params = {"offset": 60}, auth = queryoauth)
followers4 = json.loads(followers4.text)
followers4 = followers4['response']['users']
followers.extend(followers4)

followers5 = requests.get(followers_url, params = {"offset": 80}, auth = queryoauth)
followers5 = json.loads(followers5.text)
followers5 = followers5['response']['users']
followers.extend(followers5)

followers6 = requests.get(followers_url, params = {"offset": 100}, auth = queryoauth)
followers6 = json.loads(followers6.text)
followers6 = followers6['response']['users']
followers.extend(followers6)

followers7 = requests.get(followers_url, params = {"offset": 120}, auth = queryoauth)
followers7 = json.loads(followers7.text)
followers7 = followers7['response']['users']
followers.extend(followers7)

followers8 = requests.get(followers_url, params = {"offset": 140}, auth = queryoauth)
followers8 = json.loads(followers8.text)
followers8 = followers8['response']['users']
followers.extend(followers8)

# create a new list that does not contain any mutuals
non_mutuals = [i for i in followers if not (i['following'] == True)]

# define a function that will be used to softblock every follower in non_mutuals		
def softblock(x):
	block = requests.post(blocks, data=x, auth=queryoauth)
	unblock = requests.delete(blocks, data=x, auth=queryoauth)
	if block.status_code == 201 and unblock.status_code == 200:
		return 'success'
	else:
		return 'failed'

# import this library to set rate limit	
from ratelimit import limits

# tumblr api block and unblock calls are rate limited at 60 requests per minute
# decorator sets limit of 1 call per second, equivalent to 60 calls per minute
# purge() function will iterate through each item in the list, declare a variable containing the parameters needed for the block and unblock calls
# then call softblock() function
@limits(calls=1, period=1)
def purge():
	for i in range(len(non_mutuals)):
		blog = {'blocked_tumblelog': non_mutuals[i]['name']}
		softblock(blog)

#finally, call your function
purge()
