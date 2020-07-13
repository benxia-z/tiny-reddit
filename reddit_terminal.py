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
        urwid.Edit.__init__(self, caption=markup, align='center')

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


class MainView(urwid.WidgetWrap):
    body = []

    def __init__(self, title_markup):
        body = [super().__init__(urwid.Text(title_markup)), urwid.Divider()]

    def build_front_page(self, r):
        front_page = utils.get_front_page(r)
        for p in front_page:
            post = urwid.Button(p.title)
            self.body.append(urwid.AttrMap(post, None, focus_map='reversed'))
        loop.widget = urwid.ListBox(urwid.SimpleFocusListWalker(self.body))

def unhandled_input(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

    # Front Page posts
    # search
    # Subreddits
    # profile


if __name__ == "__main__":
    reddit = None

    palette = [
        ('login_banner', 'dark red', 'black'),
        ('main_footer', 'black', 'light gray'),
        ('bg', 'white', 'black'),
    ]
    auth_signals = ['authenticated']

    urwid.register_signal(AuthBox, auth_signals)

    login_prompt = AuthBox(('login_banner', u"Press 'a' to log in to Reddit"))
    footer = urwid.Text(('main_footer', u"[q] Quit | STATUS BAR"))
    main_view = MainView('Front Page')

    fill = urwid.Filler(login_prompt)
    map1 = urwid.AttrMap(fill, 'bg')
    map2 = urwid.AttrMap(footer, 'main_footer')
    frame = urwid.Frame(map1, footer=map2)
    urwid.connect_signal(login_prompt, 'authenticated', main_view.build_front_page)
    loop = urwid.MainLoop(frame, palette, unhandled_input=unhandled_input)
    loop.run()
