#!/usr/bin/env python
#coding=utf8


import time
import datetime


STATUSES = {
    'menu': 'MEMU',
    'live': 'LIVE',
}


class Controller(object):
    def __init__(self, brd, api):
        self.status = ''
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
            #st = '%s %s' % (self.status, date_show)
            #self.brd.draw_status(st)
            key = self.brd.screen.getch()

            if key == ord('q'):
                break
            if key == ord('m'):
                self.status = STATUSES['menu']
                menus = self.api.get_menus()
                self.brd.draw_menu(menus)
            elif self.status == STATUSES['menu']:
                for idx in xrange(len(self.api.avail_matches)):
                    if key == ord(str(idx+1)):
                        self.status = STATUSES['live']
                        self.api.init_match(idx)
                        self.brd.init_match()
                        lines = self.api.get_messages()
                        self.brd.update(lines, self.api.home_team, self.api.away_team)
                        self.last_update = time.time()
                        break
            elif self.status == STATUSES['live']:
                t = time.time()
                if t - self.last_update > self.wait_time or key == ord('f'):
                    lines = self.api.get_messages()
                    self.brd.update(lines, self.api.home_team, self.api.away_team)
                    self.last_update = t
            else:
                pass
            time.sleep(0.1)

