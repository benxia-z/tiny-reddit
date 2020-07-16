import praw

reddit = praw.Reddit(client_id='5oaK7xD9IW6b_w',
                     client_secret='rFpVqix-LULJf89BH6TVBY2t3no',
                     user_agent='Mockbot v1.0 (by /u/KosherCow)', )

def get_front_page_posts(reddit, sort='best', limit=5):
    '''
    return generator with a given sorting method
    '''
    front_page = reddit.front
    if sort == 'best':
        return front_page.best(limit=limit)
    elif sort == 'hot':
        return front_page.hot(limit=limit)
    elif sort == 'new':
        return front_page.new(limit=limit)
    elif sort == 'contrv.':
        return front_page.controversial(limit=limit)
    elif sort == 'top':
        return front_page.top(limit=limit)
    return front_page
        # my_subreddits = subreddits.generate_user_subreddits(reddit)
    # x = input("Press [1] to view subreddits: ")
    # if x == "1":
    #     my_subreddits = subreddits.generate_user_subreddits(reddit)
    #     print(my_subreddits)
    # return 0

if __name__ == '__main__':
    r = get_front_page(reddit)
    for p in r:
        print(p.title)