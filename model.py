import praw


class Model:
    def __init__(self, controller):
        self.controller = controller
        self.reddit_instance = controller.reddit_instance
    # TODO: move reddit api methods here
