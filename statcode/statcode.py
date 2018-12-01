#########
# GLOBALS
#########


import os
import sys
import shutil

import yaml
import urwid
from urwid.widget import BOX, FLOW, FIXED


#########
# HELPERS
#########


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
is_not_dumb = os.getenv("TERM", "dumb").lower() != "dumb"

# Scroll actions
SCROLL_LINE_UP = "line up"
SCROLL_LINE_DOWN = "line down"
SCROLL_PAGE_UP = "page up"
SCROLL_PAGE_DOWN = "page down"
SCROLL_TO_TOP = "to top"
SCROLL_TO_END = "to end"

# ASCII color codes
YELLOW = '\033[33m' if is_not_dumb else ''
RED = "\033[31m" if is_not_dumb else ''
BOLD = '\033[1m' if is_not_dumb else ''
UNDERLINE = '\033[4m' if is_not_dumb else ''
END = "\033[0m" if is_not_dumb else ''

class Scrollable(urwid.WidgetDecoration):
    # TODO: Fix scrolling behavior (works with up/down keys, not with cursor) <--- Now works with mouse though

    def sizing(self):
        return frozenset([BOX])

    def selectable(self):
        return True

    def __init__(self, widget):
        """
        Box widget (wrapper) that makes a fixed or flow widget vertically scrollable.
        """

        self._trim_top = 0
        self._scroll_action = None
        self._forward_keypress = None
        self._old_cursor_coords = None
        self._rows_max_cached = 0
        self.__super.__init__(widget)

    def render(self, size, focus=False):
        maxcol, maxrow = size

        # Render complete original widget
        ow = self._original_widget
        ow_size = self._get_original_widget_size(size)
        canv = urwid.CompositeCanvas(ow.render(ow_size, focus))
        canv_cols, canv_rows = canv.cols(), canv.rows()

        if canv_cols <= maxcol:
            pad_width = maxcol - canv_cols
            if pad_width > 0:  # Canvas is narrower than available horizontal space
                canv.pad_trim_left_right(0, pad_width)

        if canv_rows <= maxrow:
            fill_height = maxrow - canv_rows
            if fill_height > 0:  # Canvas is lower than available vertical space
                canv.pad_trim_top_bottom(0, fill_height)

        if canv_cols <= maxcol and canv_rows <= maxrow:  # Canvas is small enough to fit without trimming
            return canv

        self._adjust_trim_top(canv, size)

        # Trim canvas if necessary
        trim_top = self._trim_top
        trim_end = canv_rows - maxrow - trim_top
        trim_right = canv_cols - maxcol
        if trim_top > 0:
            canv.trim(trim_top)
        if trim_end > 0:
            canv.trim_end(trim_end)
        if trim_right > 0:
            canv.pad_trim_left_right(0, -trim_right)

        # Disable cursor display if cursor is outside of visible canvas parts
        if canv.cursor is not None:
            curscol, cursrow = canv.cursor
            if cursrow >= maxrow or cursrow < 0:
                canv.cursor = None

        # Let keypress() know if original_widget should get keys
        self._forward_keypress = bool(canv.cursor)

        return canv

    def mouse_event(self, size, event, button, col, row, focus):
        if 'press' in event.split(' '):
            if button in (4,5):
                self.keypress(size, SCROLL_PAGE_DOWN if button == 5 else SCROLL_PAGE_UP)

    def keypress(self, size, key):
        if self._forward_keypress:
            ow = self._original_widget
            ow_size = self._get_original_widget_size(size)

            # Remember previous cursor position if possible
            if hasattr(ow, "get_cursor_coords"):
                self._old_cursor_coords = ow.get_cursor_coords(ow_size)

            key = ow.keypress(ow_size, key)
            if key is None:
                return None

        # Handle up/down, page up/down, etc
        command_map = self._command_map
        if command_map[key] == urwid.CURSOR_UP:
            self._scroll_action = SCROLL_LINE_UP
        elif command_map[key] == urwid.CURSOR_DOWN:
            self._scroll_action = SCROLL_LINE_DOWN
        elif command_map[key] == urwid.CURSOR_PAGE_UP:
            self._scroll_action = SCROLL_PAGE_UP
        elif command_map[key] == urwid.CURSOR_PAGE_DOWN:
            self._scroll_action = SCROLL_PAGE_DOWN
        elif command_map[key] == urwid.CURSOR_MAX_LEFT:  # "home"
            self._scroll_action = SCROLL_TO_TOP
        elif command_map[key] == urwid.CURSOR_MAX_RIGHT:  # "end"
            self._scroll_action = SCROLL_TO_END
        else:
            return key

        self._invalidate()

    def mouse_event(self, size, event, button, col, row, focus):
        ow = self._original_widget
        if hasattr(ow, "mouse_event"):
            ow_size = self._get_original_widget_size(size)
            row += self._trim_top
            return ow.mouse_event(ow_size, event, button, col, row, focus)
        else:
            return False

    def _adjust_trim_top(self, canv, size):
        """
        Adjust self._trim_top according to self._scroll_action
        """

        action = self._scroll_action
        self._scroll_action = None

        maxcol, maxrow = size
        trim_top = self._trim_top
        canv_rows = canv.rows()

        if trim_top < 0:
            # Negative trim_top values use bottom of canvas as reference
            trim_top = canv_rows - maxrow + trim_top + 1

        if canv_rows <= maxrow:
            self._trim_top = 0  # Reset scroll position
            return

        def ensure_bounds(new_trim_top):
            return max(0, min(canv_rows - maxrow, new_trim_top))

        if action == SCROLL_LINE_UP:
            self._trim_top = ensure_bounds(trim_top - 1)
        elif action == SCROLL_LINE_DOWN:
            self._trim_top = ensure_bounds(trim_top + 1)
        elif action == SCROLL_PAGE_UP:
            self._trim_top = ensure_bounds(trim_top - maxrow + 1)
        elif action == SCROLL_PAGE_DOWN:
            self._trim_top = ensure_bounds(trim_top + maxrow - 1)
        elif action == SCROLL_TO_TOP:
            self._trim_top = 0
        elif action == SCROLL_TO_END:
            self._trim_top = canv_rows - maxrow
        else:
            self._trim_top = ensure_bounds(trim_top)

        if self._old_cursor_coords is not None and self._old_cursor_coords != canv.cursor:
            self._old_cursor_coords = None
            curscol, cursrow = canv.cursor
            if cursrow < self._trim_top:
                self._trim_top = cursrow
            elif cursrow >= self._trim_top + maxrow:
                self._trim_top = max(0, cursrow - maxrow + 1)

    def _get_original_widget_size(self, size):
        ow = self._original_widget
        sizing = ow.sizing()
        if FIXED in sizing:
            return ()
        elif FLOW in sizing:
            return size[0],

    def get_scrollpos(self, size=None, focus=False):
        return self._trim_top

    def set_scrollpos(self, position):
        self._trim_top = int(position)
        self._invalidate()

    def rows_max(self, size=None, focus=False):
        if size is not None:
            ow = self._original_widget
            ow_size = self._get_original_widget_size(size)
            sizing = ow.sizing()
            if FIXED in sizing:
                self._rows_max_cached = ow.pack(ow_size, focus)[1]
            elif FLOW in sizing:
                self._rows_max_cached = ow.rows(ow_size, focus)
            else:
                raise RuntimeError("Not a flow/box widget: %r" % self._original_widget)
        return self._rows_max_cached


class App(object):
    def __init__(self, content):
        self._palette = [
            ("menu", "black", "light cyan", "standout"),
            ("title", "default,bold", "default", "bold")
        ]

        menu = urwid.Text([u'\n', ("menu", u" Q "), ("light gray", u" Quit")])  # TODO: Make like man pages (vim input)
        layout = urwid.Frame(body=content, footer=menu)

        main_loop = urwid.MainLoop(layout, self._palette, unhandled_input=App._handle_input, handle_mouse=True)
        main_loop.run()

    @staticmethod
    def _handle_input(inp):
        if inp in ('q', 'Q'):
            raise urwid.ExitMainLoop()

def output_without_ui(content):
    size = shutil.get_terminal_size()
    canvas = content.render(size)
    text = ("\n".join(text.decode("utf-8") for text in canvas.text)).rstrip()
    print(text)

def generate_content(status_code):
    try:
        code_descriptions, num, status_code = get_yaml_dictionary(status_code)
        content = code_descriptions[status_code]
        pile = urwid.Pile([
            urwid.Text("STATCODE: The Manual for HTTP Status Codes and Headers\n", align="center"),
            urwid.Text(("title", "STATUS MESSAGE" if num else "HEADER INFO")),
            urwid.Padding(
                urwid.Text(''.join([str(status_code), ": " if num else ", Example= ", content["message"], '\n'])),
                left=5),
            urwid.Text(("title", "CATEGORY")),
            urwid.Padding(urwid.Text(''.join([content["category"], '\n'])), left=5),
            urwid.Text(("title", "DESCRIPTION")),
            urwid.Padding(urwid.Text(''.join([content["description"], '\n'])), left=5),
            urwid.Text(("title", "COPYRIGHT")),
            urwid.Padding(urwid.Text(''.join([__load_file_data(num), '\n'])), left=5),
        ])
        padding = urwid.Padding(Scrollable(pile), left=1, right=1)

        return padding
    except KeyError:  # None is used to print "not recognized", so KeyError. Other errors have nothing to do with it
        return None

def __load_file_data(num):
    copyleft = yaml.safe_load(open('/'.join([CURR_DIR, "copyright_description.yml"]), 'r'))
    if num:
        return copyleft['statuscode']
    else:
        return copyleft['headers']

def get_yaml_dictionary(status_code):
    try:
        status_code = int(status_code)
        num = True
        filename = "code_descriptions.yml"
    except (TypeError, ValueError):
        num = False
        filename = "header_descriptions.yml"
    try:
        code_descriptions = yaml.safe_load(
            open('/'.join([CURR_DIR, filename]), 'r'))
    except yaml.constructor.ConstructorError:
        print("Invalid file. Only support valid json and yaml files.")
        sys.exit(1)

    return code_descriptions, num, status_code

def print_help():
    print(''.join([BOLD, "statcode v1.0.0 – Made by @shobrook", END, '\n']))
    print("Like man pages, but for HTTP status codes.\n")
    print(''.join([UNDERLINE, "Usage:", END, " $ statcode ", YELLOW, "status_code", END]))
    print(''.join([BOLD, "-h, --help:", END, " prints this help"]))
    print(''.join([BOLD, "-a,-l, --all,--list statucode", END, " prints all codes in compact version"]))
    print(''.join([BOLD, "-a,-l, --all,--list headers", END, " prints all headers in compact version"]))
    print(''.join([BOLD, "-n, --no-ui", END, " force output without UI"]))

def print_all(status_code):
    if status_code == "statuscode":
        code_descriptions, num, status_code = get_yaml_dictionary(200)
    else:
        code_descriptions, num, status_code = get_yaml_dictionary("Accept")
    del status_code
    for k, v in code_descriptions.items():
        print(''.join([RED, str(k), ':', END, " ", v["message"] if num else ""]))


######
# MAIN
######


def main():
    if len(sys.argv) == 1 or sys.argv[1].lower() in ("-h", "--help"):
        print_help()
    elif sys.argv[1].lower() in ("-a", "-l", "--all", "--list"):
        try:
            status_code = sys.argv[2]
            if status_code not in ("statuscode", "headers"):
                print(''.join([BOLD, "Wrong parameter for this usage, see help", END]))
                return
            print_all(status_code)
        except IndexError:
            print_help()
    else:
        status_code = sys.argv[1]
        without_ui = len(sys.argv) > 2 and sys.argv[2].lower() in ("-n", "--no-ui")
        content = generate_content(status_code)

        if content:
            if without_ui or not is_not_dumb:
                output_without_ui(content)
            else:
                try:
                    App(content)  # Opens interface
                except NameError:
                    output_without_ui(content)
        else:
            print(''.join([RED, "Sorry, statcode doesn't recognize: ", status_code, END]))

    return
