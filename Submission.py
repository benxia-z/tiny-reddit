import praw


# this this logs the bot in reddit
reddit = praw.Reddit(client_id='5oaK7xD9IW6b_w',
                     client_secret='rFpVqix-LULJf89BH6TVBY2t3no',
                     user_agent='Mockbot v1.0 (by /u/KosherCow)', )
# this selects subreddit
input_subreddit = input("What subreddit do you want to look up: ")
subreddit = reddit.subreddit(input_subreddit)

#this filters the subreddit by the 10 ten (hot, new, gilded, controversial, rising, top)
while True:
    filter_subreddit = input("""What do you want to filter the subreddit by?: 
        Enter 1 to filter by Hot
        Enter 2 to filter by Top
        Enter 3 to filter by New
        Enter 4 to filter by Gilded
        Enter 5 to filter by Controversial
        Enter 6 to filter by Rising
        Enter Option Here: """)

    if filter_subreddit == "1":
       try:
            for submission in subreddit.hot(limit=10):
                    print(submission.title)  # Output: the submission's title
                    print(submission.score)  # Output: the submission's score
                    print(submission.url)    # Output: the URL the submission points to
                                             # or the submission's URL if it's a self post
            break
       except:
            print("This filter is not available for this subreddit, try another")
            continue
    if filter_subreddit == "2":
        try:
            for submission in subreddit.top(limit=10):
                print(submission.title)  # Output: the submission's title
                print(submission.score)  # Output: the submission's score
                print(submission.url)  # Output: the URL the submission points to
                # or the submission's URL if it's a self post
            break
        except:
            print("This filter is not available for this subreddit, try another")
            continue

    if filter_subreddit == "3":
        try:
            for submission in subreddit.new(limit=10):
                print(submission.title)  # Output: the submission's title
                print(submission.score)  # Output: the submission's score
                print(submission.url)  # Output: the URL the submission points to
                # or the submission's URL if it's a self post
            break
        except:
            print("This filter is not available for this subreddit, try another")
            continue

    if filter_subreddit == "4":
        try:
            for submission in subreddit.gilded(limit=10):
                print(submission.title)  # Output: the submission's title
                print(submission.score)  # Output: the submission's score
                print(submission.url)  # Output: the URL the submission points to
                # or the submission's URL if it's a self post
            break
        except:
            print("This filter is not available for this subreddit, try another")
            continue
    if filter_subreddit == "5":
        try:
            for submission in subreddit.controversial(limit=10):
                print(submission.title)  # Output: the submission's title
                print(submission.score)  # Output: the submission's score
                print(submission.url)  # Output: the URL the submission points to
                # or the submission's URL if it's a self post
            break
        except:
            print("This filter is not available for this subreddit, try another")
            continue


    if filter_subreddit == "6":
        try:
            for submission in subreddit.rising(limit=10):
                print(submission.title)  # Output: the submission's title
                print(submission.score)  # Output: the submission's score
                print(submission.url)  # Output: the URL the submission points to
                # or the submission's URL if it's a self post
            break
        except:
            print("This filter is not available for this subreddit, try another")
            continue

