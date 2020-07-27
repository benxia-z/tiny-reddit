import praw


class Model:
    def __init__(self, controller):
        self.controller = controller
        self.reddit_instance = controller.reddit_instance
    # TODO: move reddit api methods here

    def get_subreddit_posts(self, sort='hot', limit=5):
        """
        return iterator with a given sorting method
        """
        post_iterator = self.reddit_instance.front
        if sort == 'hot':
            return post_iterator.hot(limit=limit)
        elif sort == 'new':
            return post_iterator.new(limit=limit)
        elif sort == 'rising':
            return post_iterator.rising(limit=limit)
        elif sort == 'controversial':
            return post_iterator.controversial(limit=limit)
        elif sort == 'top':
            return post_iterator.top(limit=limit)
        return post_iterator

    def get_post_content(self, post):
        """
        :param post: self.reddit_instance.submission
        :return:
        """
        post_content = {'selftext': post.selftext,
                        'url': post.url,
                        'comments': post.comments}
        return post_content
