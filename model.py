import praw


class Model:
    def __init__(self, controller):
        self.controller = controller
        self.reddit_instance = controller.reddit_instance
    # TODO: move reddit api methods here

    def get_front_page_posts(self, sort='hot', limit=5):
        '''
        return generator with a given sorting method
        '''
        front_page = self.reddit_instance.front
        if sort == 'hot':
            return front_page.hot(limit=limit)
        elif sort == 'new':
            return front_page.new(limit=limit)
        elif sort == 'contrv.':
            return front_page.controversial(limit=limit)
        elif sort == 'top':
            return front_page.top(limit=limit)
        return front_page
