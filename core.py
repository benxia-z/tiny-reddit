import urwid

from authentication import get_reddit_instance
from model import Model
from tui import View


class Controller:
    """The controller sets up the model/view and runs the application."""

    def __init__(self):
        # TODO: themes?
        self.loop = None
        self.reddit_instance = get_reddit_instance()
        self.model = Model(self)
        self.view = View(self)

    def login(self):
        self.reddit_instance = get_reddit_instance(read_only=False)
        self.model.reddit_instance = self.reddit_instance

    def redraw_screen(self, w):
        self.loop.widget = w

    def show_popup(self):
        # TODO: add implementation for popups here
        pass

    def close_popup(self):
        pass

    def log_off(self):
        pass

    def main(self):
        palette = [
            ('login_banner', 'dark red', 'black'),
            ('main_footer', 'black', 'light gray'),
            ('bg', 'white', 'black'),
            ('reversed', 'standout', '')
        ]

        self.loop = urwid.MainLoop(self.view, palette, unhandled_input=self.view.unhandled_input)
        self.loop.run()

if __name__ == "__main__":
    controller = Controller()
    controller.main()



