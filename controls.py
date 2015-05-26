#!/usr/bin/env python
#coding=utf8


import time
import datetime


STATUSES = {
    'menu': 'M',
    'live': 'L',
}


class Controller(object):
    def __init__(self, brd, api):
        self.status = None
        self.wait_time = 5
        self.last_update = 0
        self.brd = brd
        self.api = api

    def get_now(self):
        dt = datetime.datetime.now()
        date_show = '%04d年%02d月%02d日 %02d:%02d:%02d' % (
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second
        )
        return date_show

    def start(self):
        self.status = STATUSES['menu']
        menus = self.api.get_menus()
        self.brd.draw_menu(menus)

        while True:
            date_show = self.get_now()
            self.brd.draw_status(date_show)
            key = self.brd.screen.getch()

            if key == ord('q'):
                break
            if key == ord('m'):
                menus = self.api.get_menus()
                self.brd.draw_menu(menus)
            elif self.status == STATUSES['menu']:
                if key == ord(' '):
                    self.status = STATUSES['live']
            elif self.status == STATUSES['live']:
                t = time.time()
                if t - self.last_update > self.wait_time or key == ord('f'):
                    lines = self.api.get_messages()
                    self.brd.update(lines)
                    self.last_update = t
            else:
                pass
