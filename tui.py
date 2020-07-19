import urwid

class AuthBox(urwid.Edit):
    def __init__(self, markup):
        super().__init__(caption=markup, align='center')


class View(urwid.WidgetWrap):

    def __init__(self, controller):
        self.controller = controller
        self.model = controller.model
        self.post_content = None
        self.header = None
        self.frame = None
        self.footer = None
        self.tab_menu = None
        self.body = []
        self.tab_list = ['hot', 'new', 'controversial', 'top']
        # registering custom authentication signals
        self.auth_signals = ['authenticated']
        super().__init__(self.main_window())

    def generate_header(self, title_markup, header):
        self.body = [urwid.Text(title_markup), urwid.Divider(), header, urwid.Divider()]

    def build_front_page(self):
        front_page = self.model.get_front_page_posts()
        self.update_posts(front_page, redraw_screen=True)

    def update_posts(self, page, redraw_screen=False):
        for p in page:
            post = FixedButton(p.title + '\n' + 'submitted x hours ago by {} to {}'.format(p.author.name, p.subreddit) +
                               '\n' + '{} comments'.format(p.num_comments) + '\n')
            self.body.append(urwid.AttrMap(post, None, focus_map='reversed'))
        self.post_content = urwid.ListBox(urwid.SimpleFocusListWalker(self.body))
        self.frame = urwid.Frame(self.post_content, footer=self.footer)
        if not redraw_screen:
            self.controller.redraw_screen(self.frame)

    def refresh_front_page(self, tab_button, tab_name='hot', redraw_screen=False):
        front_page = self.model.get_front_page_posts(tab_name)
        self.body = []
        self.generate_header('Front Page', self.header)
        self.update_posts(front_page, redraw_screen)

    def main_window(self):
        self.tab_menu = urwid.Columns([], dividechars=1)
        for tab_name in self.tab_list:
            tab = FixedButton(tab_name)
            urwid.connect_signal(tab, 'click', self.refresh_front_page, tab_name)
            self.tab_menu.contents.append((urwid.AttrMap(tab, None, focus_map='reversed'),
                                           self.tab_menu.options(width_type=urwid.GIVEN, width_amount=len(tab_name)+4)))
        # TODO: change to function that allows multiple arguments
        self.header = urwid.Columns([self.tab_menu])
        self.generate_header('Front Page', self.header)
        self.footer = urwid.Text(('main_footer', u"[q] Quit | [a] Login"))
        map2 = urwid.AttrMap(self.footer, 'main_footer')
        self.build_front_page()
        self.frame = urwid.Frame(self.post_content, footer=map2)
        urwid.register_signal(self, self.auth_signals)
        return self.frame

    def keypress(self, size, key):
        if key == 'a':
            self.controller.login()
            self.refresh_front_page('d', redraw_screen=False)
        if key == 'b':
            urwid.emit_signal(self, 'authenticated')
            return
        if key == 'c':
            return urwid.Filler(urwid.Text('Test'))
        if key == 'q':
            raise urwid.ExitMainLoop()
        return super().keypress(size, key)

    def emit_auth_signal(self, r):
        urwid.emit_signal(self, 'authenticated', r)

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()


class FixedLabel(urwid.SelectableIcon):
    # The terminal cursor normally appears in buttons, this removes the cursor
    def __init__(self, text):
        curs_pos = len(text) + 1
        urwid.SelectableIcon.__init__(self, text, cursor_position=curs_pos)


class FixedButton(urwid.WidgetWrap):
    # Implementing fixed button label
    _selectable = True
    signals = ['click']

    def __init__(self, label):
        self.label = FixedLabel(label)
        display_widget = self.label
        urwid.WidgetWrap.__init__(self, urwid.AttrMap(display_widget, None, focus_map='reversed'))

    def keypress(self, size, key):
        if self._command_map[key] != urwid.ACTIVATE:
            return key

        self._emit('click')

    def set_label(self, new_label):
        self.label.set_text(str(new_label))