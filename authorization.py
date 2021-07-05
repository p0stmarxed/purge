#!/bin/env python

# import libraries
import requests
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1

import webbrowser

# global vars
resource_owner_key = ''
resource_owner_secret = ''

# authorize
def authorize(client_key, client_secret):
    base_auth_url = 'https://www.tumblr.com/oauth/'
    request_token_url = base_auth_url + 'request_token'
    authorize_url = base_auth_url + 'authorize'

    oauth = OAuth1Session(client_key, client_secret=client_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)

    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    authorization_url = oauth.authorization_url(authorize_url)
    webbrowser.open(authorization_url)

    redirect_response = input('Paste the full redirect URL here: ')
    oauth_response = oauth.parse_authorization_response(redirect_response)

    verifier = oauth_response.get('oauth_verifier')

    access_token_url = base_auth_url + 'access_token'
    oauth = OAuth1Session(client_key,
        client_secret=client_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    return oauth_tokens
