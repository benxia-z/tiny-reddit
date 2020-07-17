import sys
import os
import curses
import login
import praw
import refresh
import utils
import urwid

class AuthBox(urwid.Edit):

    def __init__(self, markup):
        super().__init__(caption=markup, align='center')

    def keypress(self, size, key):
        if key == 'a':
            reddit_instance = refresh.main()
            if reddit_instance:
                self.emit_auth_signal(reddit_instance)
        if key == 'b':
            urwid.emit_signal(self, 'authenticated')
        if key == 'c':
            loop.widget = urwid.Filler(urwid.Text('Test'))
        if key == 'q':
            raise urwid.ExitMainLoop()

    def emit_auth_signal(self, r):
        urwid.emit_signal(self, 'authenticated', r)


class MainView:
    body = []
    post_content = None
    reddit_instance = None

    def generate_header(self, title_markup, header):
        self.body = [urwid.Text(title_markup), urwid.Divider(), header, urwid.Divider()]

    def retrieve_reddit_instance(self, r):
        self.reddit_instance = r
        self.build_front_page(self.reddit_instance)

    def build_front_page(self, r, title_markup='', header=[]):
        front_page = utils.get_front_page_posts(r)
        self.update_posts(front_page)

    def update_posts(self, page):
        for p in page:
            post = urwid.Button(p.title)
            self.body.append(urwid.AttrMap(post, None, focus_map='reversed'))
        self.post_content = urwid.ListBox(urwid.SimpleFocusListWalker(self.body))
        loop.widget = urwid.Frame(self.post_content, footer=map2)

    def refresh_front_page(self, tab_button, tab_name='best'):
        front_page = utils.get_front_page_posts(self.reddit_instance, tab_name)
        self.body = []
        self.generate_header('Front Page', front_header)
        self.update_posts(front_page)



class TabMenu(urwid.Columns):
    def __init__(self):
        super().__init__([], dividechars=1)

    def generate_tabs(self, tabs):
        for tab in tabs:
            tab = SubredditTab(tab)
            self.contents.append((urwid.AttrMap(tab, None, focus_map='reversed'), self.options()))


class SubredditTab(urwid.Button):
    def __init__(self, tab_name):
        super().__init__(tab_name)
        urwid.connect_signal(self, 'click', main_view.refresh_front_page, tab_name)


class Header(urwid.Columns):
    def __init__(self, header_widgets):
        super().__init__(header_widgets)


def unhandled_input(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

    # Front Page posts
    # search
    # Subreddits
    # profile


if __name__ == "__main__":
    palette = [
        ('login_banner', 'dark red', 'black'),
        ('main_footer', 'black', 'light gray'),
        ('bg', 'white', 'black'),
    ]

    # registering custom authentication signals
    auth_signals = ['authenticated']

    urwid.register_signal(AuthBox, auth_signals)

    # auth page widget
    login_prompt = AuthBox(('login_banner', u"Press 'a' to log in to Reddit"))
    footer = urwid.Text(('main_footer', u"[q] Quit | STATUS BAR"))

    # front page view created here
    main_view = MainView()
    front_tabs = TabMenu()
    front_tabs.generate_tabs(['best', 'hot', 'new', 'contrv.', 'top'])
    print(front_tabs)
    front_header = Header([front_tabs])
    main_view.generate_header('Front Page', front_header)

    # auth page display
    fill = urwid.Filler(login_prompt)
    map1 = urwid.AttrMap(fill, 'bg')
    map2 = urwid.AttrMap(footer, 'main_footer')
    frame = urwid.Frame(map1, footer=map2)

    # connecting authentication signal
    urwid.connect_signal(login_prompt, 'authenticated', main_view.retrieve_reddit_instance)
    loop = urwid.MainLoop(frame, palette, unhandled_input=unhandled_input)
    loop.run()
