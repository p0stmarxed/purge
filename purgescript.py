#!/bin/env python

# import libraries
import sys, getopt

# import local modules
import authorization
import purge

# global vars - to avoid having a billion params everywhere
username = ''
number_to_block = 0
client_key = ''
client_secret = ''
nice_mode = False

def main():
    long_args = ["nice", "username=", "key=", "secret=", "max="]
    global username, number_to_block, client_key, client_secret, nice_mode

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:m:k:s:", long_args)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    
    for o, a in opts:
        if o in ("--nice"):
            nice_mode = True
        elif o in ("-u", "--username"):
            username = a
        elif o in ("-m", "--max"):
            number_to_block = int(a)
            if not isinstance(number_to_block, int):
                print("number of followers to block must be an integer")
                sys.exit(2)
        elif o in ("-k", "--key"):
            client_key = a
        elif o in ("-s", "--secret"):
            client_secret = a
        else:
            assert False, "unhandled option"

    if not username or not number_to_block:
        print("username and number of followers to block required")
        sys.exit(1)
    if not client_key or not client_secret:
        print("client key and secret required")
        sys.exit(1)

    access_token = authorization.authorize(client_key, client_secret)
    resource_owner_key = access_token['oauth_token']
    resource_owner_secret = access_token['oauth_token_secret']

    tokens = {
        "client_key": client_key,
        "client_secret": client_secret,
        "resource_owner_key": resource_owner_key,
        "resource_owner_secret": resource_owner_secret
    }

    purge.purge(tokens, username, number_to_block, nice_mode)

if __name__ == "__main__":
    main()
