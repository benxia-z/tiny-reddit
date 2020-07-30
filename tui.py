import urwid


class View(urwid.WidgetWrap):

    def __init__(self, controller):
        self.screen = controller.screen
        self.controller = controller
        self.model = controller.model
        self.height, self.width = self.screen.get_cols_rows()
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
        self.page_content_list = []
        self.post_generator = self.model.get_subreddit_posts('hot')
        self.page_content = None
        self.page_number = 0
        self.max_pages = 1
        self.sub_end_reached = False
        self.tab_list = ['hot', 'new', 'rising', 'controversial', 'top']
        # registering custom authentication signals
        self.auth_signals = ['authenticated']
        super().__init__(self.main_window())

    def update_posts(self, post_generator, redraw_screen=False):
        # TODO: need to set post generator as a attribute so we can keep pages until refreshed
        self.post_content = urwid.BoxAdapter(PostBody(self, post_generator), 43)
        self.header.update_content(self.page_number)
        self.page_content = urwid.ListBox(urwid.SimpleFocusListWalker(self.header.header_content + [self.post_content]))
        self.page_content.set_focus(4)
        self.frame.contents['body'] = (self.page_content, None)
        self.page_list.append(self.frame.contents['body'])

    def reset_content(self):
        self.page_list = []
        self.page_content_list = []
        self.post_generator = self.model.get_subreddit_posts('hot')
        self.page_content = None
        self.page_number = 0
        self.max_pages = 1
        self.sub_end_reached = False

    def refresh_front_page(self, tab_button, tab_name='hot', redraw_screen=False):
        self.reset_content()
        self.header.generate_tabs(self)
        self.post_generator = self.model.get_subreddit_posts(tab_name)
        self.page_content_list += self.header.header_content
        self.update_posts(self.post_generator, redraw_screen)

    def main_window(self):
        # initialize front page view
        self.header = Header(self, 'Front Page', self.tab_list)
        self.page_content_list += self.header.header_content
        self.post_generator = self.model.get_subreddit_posts()
        self.post_content = urwid.BoxAdapter(PostBody(self, self.post_generator), 43)
        self.page_content = urwid.ListBox(urwid.SimpleFocusListWalker(self.header.header_content + [self.post_content]))
        self.page_content.set_focus(4)
        self.frame = urwid.Frame(self.page_content, footer=self.sub_footer)
        self.page_list.append(self.frame.contents['body'])
        urwid.register_signal(self, self.auth_signals)
        return self.frame

    def move_next_page(self, post_body):
        if not self.sub_end_reached or self.page_number + 1 != self.max_pages:
            self.page_number += 1
        if self.page_number == self.max_pages:
            if not self.sub_end_reached:
                self.max_pages += 1
                self.update_posts(self.post_generator)
        else:
            self.frame.contents['body'] = self.page_list[self.page_number]

    def move_prev_page(self, post_body):
        if self.page_number != 0:
            self.page_number -= 1
            self.frame.contents['body'] = self.page_list[self.page_number]

    def keypress(self, size, key):
        if key == 'a':
            self.controller.login()
            self.refresh_front_page(None)
        if key == 'q':
            raise urwid.ExitMainLoop()
        return super().keypress(size, key)


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
        title = post.title
        if len(title) >= view.height - 7:
            title = title[:view.height - 10] + '...'
        self.post_content = urwid.AttrMap(FixedButton(
            title + '\n' + 'submitted x hours ago by {} to r/{}'.format(post.author.name, post.subreddit) +
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


class PostBody(urwid.ListBox):
    signals = ['next', 'prev']

    def __init__(self, view, post_generator):
        post_list = []
        for p in range(10):
            # TODO: calculate time since post creation
            try:
                post = Post(view, post_generator.__next__())
                post_list.append(post)
            except StopIteration:
                view.sub_end_reached = True
                break
        super().__init__(urwid.SimpleFocusListWalker(post_list))
        urwid.connect_signal(self, 'next', view.move_next_page)
        urwid.connect_signal(self, 'prev', view.move_prev_page)

    def keypress(self, size, key):
        if self._command_map[key] == urwid.CURSOR_RIGHT:
            self._emit('next')
        if self._command_map[key] == urwid.CURSOR_LEFT:
            self._emit('prev')
        return super().keypress(size, key)


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
            self.view.controller.redraw_screen(self.view)
        return super().keypress(size, key)

    # TODO: comment ui


class Header:
    # TODO: allow users to switch subreddits
    def __init__(self, view, title_markup, tab_list):
        # self.view = view
        self.tab_list = tab_list
        self.sub_name = 'Front Page'
        self.tab_content = None
        self.generate_tabs(view)
        self.tab_menu = urwid.Columns([self.tab_content])
        self.header_content = [urwid.Text(title_markup),
                               urwid.Divider(),
                               self.tab_menu,
                               urwid.Text('Page {}'.format(view.page_number), align='right')]

    def generate_tabs(self, view):
        # TODO: add tab for switching time period for tab
        self.tab_content = urwid.Columns([], dividechars=1)
        for tab_name in self.tab_list:
            tab = FixedButton(tab_name)
            urwid.connect_signal(tab, 'click', view.refresh_front_page, tab_name)
            self.tab_content.contents.append((urwid.AttrMap(tab, None, focus_map='reversed'),
                                              self.tab_content.options(width_type=urwid.GIVEN,
                                              width_amount=len(tab_name)+4)))

    def update_content(self, page_number, title_markup='Front Page'):
        self.header_content = [urwid.Text(title_markup),
                               urwid.Divider(),
                               self.tab_menu,
                               urwid.Text('Page {}'.format(page_number), align='right')]
