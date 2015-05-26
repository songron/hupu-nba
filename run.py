#!/usr/bin/env python
#coding=utf8


import time
from board import Board
from hupuapi import APIClient
from controls import Controller


def main():
    brd = Board()
    api = APIClient()
    ctr = Controller(brd, api)
    try:
        ctr.start()
    except Exception as e:
        pass
    finally:
        brd.exit()


if __name__ == '__main__':
    main()
