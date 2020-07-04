
"""This example demonstrates the flow for retrieving a refresh token.

In order for this example to work your application's redirect URI must be set
to http://localhost:8080.

This tool can be used to conveniently create refresh tokens for later use with
your web application OAuth2 credentials.

"""

import sys
import login
from login import client_id, client_secret, user_agent
import subreddits
import praw
from curses import wrapper
from os import path

def main():
    """Provide the program's entry point when directly executed."""
    mode = 'r+' if path.exists("userdata.txt") else 'w+'
    with open("userdata.txt", 'r+') as f:
        if len(f.read()) == 0:
            user_data = login.main()
            refresh_token = user_data["refresh_token"]
            reddit = user_data["reddit"]
            f.write(refresh_token)
        else:
            f.seek(0)
            refresh_token = f.readline()
            reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                refresh_token=refresh_token,
                user_agent=user_agent,
            )
        return reddit

    # my_subreddits = subreddits.generate_user_subreddits(reddit)
    # x = input("Press [1] to view subreddits: ")
    # if x == "1":
    #     my_subreddits = subreddits.generate_user_subreddits(reddit)
    #     print(my_subreddits)
    # return 0


if __name__ == "__main__":
    main()
