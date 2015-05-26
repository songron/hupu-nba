#!/usr/bin/env python
#coding=utf8


import time
from board import Board
from hupuapi import APIClient


def nba_live(b, api):
    while True:
        key = b.screen.getch()
        if key == ord('q'):
            break
        if key == ord('f'):
            lines = api.get_messages()
            b.update(lines)


def main():
    b = Board()
    api = APIClient()
    try:
        nba_live(b, api)
    except Exception as e:
        pass
    finally:
        b.exit()


if __name__ == '__main__':
    main()
