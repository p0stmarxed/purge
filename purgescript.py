#!/bin/env python

# import libraries
import sys, getopt

# import local modules
import authorization
import purge

# global vars - to avoid having a billion params everywhere
username = ''
max_followers_to_consider = 0
client_key = ''
client_secret = ''

def main():
    long_args = ["help", "username=", "key=", "secret=", "max="]
    global username, max_followers_to_consider, client_key, client_secret

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:m:k:s:", long_args)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    
    for o, a in opts:
        if o in ("-u", "--username"):
            username = a
        elif o in ("-m", "--max"):
            max_followers_to_consider = int(a)
            if not isinstance(max_followers_to_consider, int):
                print("max to block must be an integer")
                sys.exit(2)
        elif o in ("-k", "--key"):
            client_key = a
        elif o in ("-s", "--secret"):
            client_secret = a
        else:
            assert False, "unhandled option"

    if not username or not max_followers_to_consider:
        print("username and max followers to block required")
        sys.exit(1)
    if not client_key or not client_secret:
        print("client key and secret required")
        sys.exit(1)

    queryoauth = authorization.authorize(client_key, client_secret)
    purge.purge(queryoauth)

if __name__ == "__main__":
    main()