import urwid


class View(urwid.WidgetWrap):

    def __init__(self, controller):
        self.controller = controller
        self.model = controller.model
        self.post_content = None
        self.header = None
        self.frame = None
        self.sub_footer = urwid.AttrMap(urwid.Text(('main_footer', u"[q] Quit | [a] Login")), 'main_footer')
        self.post_footer = urwid.AttrMap(urwid.Text(('post_footer',
                                                     u'[q] Quit | '
                                                     u'[c] Comment | '
                                                     u'[b] Back')), 'main_footer')
        self.tab_menu = None
        self.page_list = []
        self.page_content = None
        self.tab_list = ['hot', 'new', 'rising', 'controversial', 'top']
        # registering custom authentication signals
        self.auth_signals = ['authenticated']
        super().__init__(self.main_window())

    def generate_header(self):
        # currently appends the header to page content
        self.page_list += self.header.header_content

    def build_front_page(self):
        # creates a front page generator and assigns the loop widget to the frame
        front_page = self.model.get_subreddit_posts()
        self.update_posts(front_page, redraw_screen=True)

    def update_posts(self, post_generator, redraw_screen=False):
        # TODO: need to set post generator as a attribute so we can keep pages until refreshed
        self.post_content = PostBody(self, post_generator).post_list
        self.page_list = self.header.header_content + self.post_content
        self.page_content = urwid.ListBox(urwid.SimpleFocusListWalker(self.page_list))
        self.frame = urwid.Frame(self.page_content, footer=self.sub_footer)
        if not redraw_screen:
            self.controller.redraw_screen(self.frame)

    def refresh_front_page(self, tab_button, tab_name='hot', redraw_screen=False):
        self.page_list = []
        self.header.generate_tabs()
        front_page = self.model.get_subreddit_posts(tab_name)
        self.generate_header()
        self.update_posts(front_page, redraw_screen)

    def main_window(self):
        self.header = Header(self, 'Front Page', self.tab_list)
        self.generate_header()
        self.build_front_page()
        self.frame = urwid.Frame(self.page_content, footer=self.sub_footer)
        urwid.register_signal(self, self.auth_signals)
        return self.frame

    def keypress(self, size, key):
        if key == 'a':
            self.controller.login()
            self.refresh_front_page(None, redraw_screen=False)
        if key == 'b':
            urwid.emit_signal(self, 'authenticated')
            return
        if key == 'c':
            return
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
        super().__init__(urwid.AttrMap(display_widget, None, focus_map='reversed'))

    def keypress(self, size, key):
        if self._command_map[key] != urwid.ACTIVATE:
            return key

        self._emit('click')

    def set_label(self, new_label):
        self.label.set_text(str(new_label))


class Post(urwid.WidgetWrap):
    signals = ['click']

    def __init__(self, view, post):
        # TODO: calculate time since post creation
        # TODO: add markup to text for username, subreddit, etc.
        self.post_content = urwid.AttrMap(FixedButton(
            post.title + '\n' + 'submitted x hours ago by {} to r/{}'.format(post.author.name, post.subreddit) +
            '\n' + '{} comments'.format(post.num_comments) + '\n'), None, focus_map='reversed')
        # self.height = self.post_content.rows() - 1
        self.left_bar = None
        # TODO: change score so large numbers are reduced, e.g. 123456 -> 123.5k
        self.left_col = urwid.Text(('{}'.format(post.score)), align='center')
        super().__init__(urwid.Columns([]))
        super().__init__(urwid.Columns([('fixed', 7, self.left_col), self.post_content]))
        urwid.connect_signal(self, 'click', self.switch_to_post_view, user_args=[view, post])

    def keypress(self, size, key):
        if self._command_map[key] != urwid.ACTIVATE:
            return key
        self._emit('click')

    def switch_to_post_view(self, view, post, button):
        post_view = PostView(view, post)
        view.controller.redraw_screen(urwid.Frame(post_view, footer=view.post_footer))


class PostBody:
    def __init__(self, view, post_generator):
        self.post_list = []
        for p in post_generator:
            # TODO: calculate time since post creation
            post = Post(view, p)
            self.post_list.append(post)


class PostView(urwid.ListBox):
    def __init__(self, view, post):
        self.view = view
        post_widget_body = []
        post_body = self.view.model.get_post_content(post)
        if post_body['selftext']:
            post_widget_body.append(urwid.Text(post_body['selftext']))
        else:
            post_widget_body.append(urwid.Text(post_body['url']))
        super().__init__(urwid.SimpleFocusListWalker(post_widget_body))

    def keypress(self, size, key):
        if key == 'b':
            self.view.controller.redraw_screen(self.view.frame)
        return super().keypress(size, key)

    # TODO: comment ui


class Header:
    # TODO: allow users to switch subreddits
    def __init__(self, view, title_markup, tab_list):
        self.view = view
        self.tab_list = tab_list
        self.sub_name = 'Front Page'
        self.tab_content = None
        self.generate_tabs()
        self.tab_menu = urwid.Columns([self.tab_content])
        self.header_content = [urwid.Text(title_markup), urwid.Divider(), self.tab_menu, urwid.Divider()]

    def generate_tabs(self):
        # TODO: add tab for switching time period for tab
        self.tab_content = urwid.Columns([], dividechars=1)
        for tab_name in self.tab_list:
            tab = FixedButton(tab_name)
            urwid.connect_signal(tab, 'click', self.view.refresh_front_page, tab_name)
            self.tab_content.contents.append((urwid.AttrMap(tab, None, focus_map='reversed'),
                                              self.tab_content.options(width_type=urwid.GIVEN,
                                              width_amount=len(tab_name)+4)))

