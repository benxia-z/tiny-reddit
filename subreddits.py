def generate_user_subreddits(reddit):
    subreddits = []
    for subreddit in reddit.user.subreddits():
        subreddits.append(subreddit.display_name)
    return subreddits
