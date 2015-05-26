#coding=utf8


import curses
import time
import locale
locale.setlocale(locale.LC_ALL, '')
# code = locale.getpreferredencoding()


class Board(object):

    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.screen.keypad(1)
        self.screen.nodelay(1)
        curses.start_color()
        self.screen.refresh()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        self.cache_size = 10
        self.cache_lines = []

    def update_cache(self, lines):
        if not self.cache_lines:
            self.cache_lines = lines[:self.cache_size]
        else:
            temp_lines = self.cache_lines
            self.cache_lines = []
            for msg in lines:
                sid = msg[0]
                if len(self.cache_lines) >= self.cache_size or sid <= temp_lines[0][0]:
                    break
                self.cache_lines.append(msg)

            for msg in temp_lines:
                if len(self.cache_lines) >= self.cache_size:
                    break
                self.cache_lines.append(msg)

    def draw_status(self, status):
        self.screen.addstr(0, 2, '%s' % (status, ), curses.color_pair(1))
        self.screen.refresh()

    def draw_menu(self, menus):
        self.screen.erase()
        self.screen.addstr(1, 25, '近期比赛', curses.color_pair(2))
        x, y = 3, 2
        for i, (_datetime, _teams, _info) in enumerate(menus):
            self.screen.addstr(x, y, '[%d]' % (i+1,), curses.color_pair(1))
            self.screen.addstr(x, y+5, _datetime, curses.color_pair(1))
            self.screen.addstr(x, y+30, _teams, curses.color_pair(1))
            self.screen.addstr(x, y+50, _info, curses.color_pair(1))
            x += 2
        self.screen.refresh()

    def draw_header(self):
        x, y = 1, 1
        self.screen.addstr(x, y, '本节剩余', curses.color_pair(2))
        self.screen.addstr(x, y+9, '当前比分', curses.color_pair(2))
        self.screen.addstr(x, y+19, '球队', curses.color_pair(2))
        self.screen.addstr(x, y+25, '比赛信息', curses.color_pair(2))

    def update(self, lines):
        if not lines:
            return
        if self.cache_lines and self.cache_lines[0][0] >= lines[0][0]:
            return
        self.update_cache(lines)

        self.screen.erase()
        self.draw_header()
        x, y = 3, 2
        for sid, residual, scores, team, content in self.cache_lines:
            self.screen.move(x, y)
            self.screen.clrtoeol()
            self.screen.addstr(x, y, residual, curses.color_pair(1))
            self.screen.addstr(x, y+9, scores, curses.color_pair(1))
            self.screen.addstr(x, y+18, team, curses.color_pair(1))
            self.screen.addstr(x, y+24, content, curses.color_pair(1))
            x += 1
        self.screen.refresh()

    def exit(self):
        self.screen.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


if __name__ == '__main__':
    pass
