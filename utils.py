import praw

reddit = praw.Reddit(client_id='5oaK7xD9IW6b_w',
                     client_secret='rFpVqix-LULJf89BH6TVBY2t3no',
                     user_agent='Mockbot v1.0 (by /u/KosherCow)', )

def get_front_page(reddit, limit=5):
    '''
    return generator
    '''
    front_page = reddit.front.hot(limit=limit)
    return front_page
        # my_subreddits = subreddits.generate_user_subreddits(reddit)
    # x = input("Press [1] to view subreddits: ")
    # if x == "1":
    #     my_subreddits = subreddits.generate_user_subreddits(reddit)
    #     print(my_subreddits)
    # return 0

if __name__ == '__main__':
    get_front_page(reddit)