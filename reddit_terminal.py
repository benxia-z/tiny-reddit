import urwid

from core import Controller
from tui import View
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

    # auth page widget
    footer = urwid.Text(('main_footer', u"[q] Quit | [a] Login |"))

    # front page view created here
    # main_view = MainView()
    # front_tabs = TabMenu()
    # front_tabs.generate_tabs(['best', 'hot', 'new', 'contrv.', 'top'])
    # print(front_tabs)
    # front_header = Header([front_tabs])
    # main_view.generate_header('Front Page', front_header)

    # auth page display
    # fill = urwid.Filler(login_prompt)
    # map1 = urwid.AttrMap(fill, 'bg')
    # map2 = urwid.AttrMap(footer, 'main_footer')
    # frame = urwid.Frame(map1, footer=map2)
    controller = Controller()
    view = controller.view
    loop = urwid.MainLoop(view, palette, unhandled_input=view.unhandled_input)
    loop.run()
