import curses

CHECKBOX_INDEX = -1
CHECKBOX_POSITION = 1
CHECKBOX_WIDTH = 4


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


def initialize():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr


def draw_screen(scr, items, position):
    for i in range(len(items)):
        item = items[i]
        scr.addstr(i, 0, str(item))

    scr.move(*position.to_screen())
    scr.refresh()


def finalize(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def main():
    stdscr = initialize()
    items = [Item('', False), Item('', False), Item('', True)]
    movement = {'h': Position(0, -1), 'j': Position(1, 0), 'k': Position(-1, 0), 'l': Position(0, 1)}
    position = Position(0, 0)

    while True:
        draw_screen(stdscr, items, position)
        key = stdscr.getkey()

        if key == 'q':
            break
        elif key in movement:
            new_position = position + movement[key]
            if 0 <= new_position.y < len(items):
                if CHECKBOX_INDEX <= new_position.x <= len(items[new_position.y].text):
                    position = new_position


    finalize(stdscr)

if __name__ == '__main__':
    main()