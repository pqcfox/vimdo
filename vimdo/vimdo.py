import curses
import enum

CHECKBOX_INDEX = -1
CHECKBOX_POSITION = 1
CHECKBOX_WIDTH = 4
KEY_ESCAPE = 27


class Mode(enum.Enum):
    normal = 1
    insert = 2
    replace = 3


class Item:
    def __init__(self, text, completed=False):
        self.text = text
        self.completed = completed

    def __str__(self):
        format_string = '[x] {}' if self.completed else '[ ] {}'
        return format_string.format(self.text)


class Position:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __add__(self, other):
        new_y, new_x = self.y + other.y, self.x + other.x
        return Position(new_y, new_x)

    def to_screen(self):
        screen_y = self.y
        screen_x = CHECKBOX_POSITION if self.x == CHECKBOX_INDEX else CHECKBOX_WIDTH + self.x
        return screen_y, screen_x


MODE_STRINGS = {Mode.normal: '',
                Mode.insert: '-- INSERT --',
                Mode.replace: '-- REPLACE --'}

MOVE_KEYS = {ord('h'): Position(0, -1),
             ord('j'): Position(1, 0),
             ord('k'): Position(-1, 0),
             ord('l'): Position(0, 1)}


def initialize():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    return stdscr


def draw_screen(scr, items, position, mode):
    scr.clear()

    for i in range(len(items)):
        item = items[i]
        scr.addstr(i, 0, str(item))

    max_y = scr.getmaxyx()[0] - 1
    scr.addstr(max_y, 0, MODE_STRINGS[mode])

    scr.refresh()
    scr.move(*position.to_screen())


def safe_move(position, move, items):
    new_position = position + move
    if 0 <= new_position.y < len(items):
        if CHECKBOX_INDEX <= new_position.x <= len(items[new_position.y].text):
            return new_position
    return position


def finalize():
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def main():
    stdscr = initialize()
    items = [Item('', False), Item('', False), Item('', True)]
    mode = Mode.normal
    position = Position(0, 0)

    while True:
        draw_screen(stdscr, items, position, mode)
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif mode == Mode.normal and key == ord('i'):
            mode = Mode.insert
        elif mode == Mode.normal and key == ord('r'):
            mode = Mode.replace
        elif key == KEY_ESCAPE:
            mode = Mode.normal
        elif key in MOVE_KEYS:
            position = safe_move(position, MOVE_KEYS[key], items)

    finalize()

if __name__ == '__main__':
    main()