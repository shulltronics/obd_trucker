#!/bin/python

import time
import curses
import curses_helpers as ch
from elm327 import Elm327
### Global variables ###
from settings import *


def main(stdscr):
    
    # main curses configuration
    # turn off cursor
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # set timeout for gathering character input
    stdscr.timeout(gCURSES_CH_TIMEOUT)
    ch.display_header(stdscr)
    stdscr.refresh()

    elm.init()

    # make the main window for data display
    (y, x) = stdscr.getyx()
    mw = curses.newwin(curses.LINES - y - 3, curses.COLS - x - 4, y + 1, x + 2)
    mw.refresh()
    

    # main loop
    t0 = time.time()
    dt = 1
    while True:
        # see if user input a character and handle it
        try:
            c = stdscr.getkey()
            if c == 's':
                ch.display_legend(mw)
            elif c == 'q':
                break
            elif c == 'c':
                mw.clear()
            elif c == 'v':
                voltage = elm.request_voltage()
                mw.addstr(f'> {voltage}')
                (y, x) = mw.getyx()
                mw.move(y+1, 0)
            elif c == 'r':
                ver = elm.reset()
                mw.addstr(f'> {ver}')
                (y, x) = mw.getyx()
                mw.move(y+1, 0)
                elm.init()
            elif c == 'h':
                header = b'C410F1'
                hr = elm.set_header(header)
                mw.addstr(f'> {hr}')
                (y, x) = mw.getyx()
                mw.move(y+1, 0)
            elif c == 'm':
                r = elm.request_pid(0x221440)
                mw.addstr(f'> {r}')
                (y, x) = mw.getyx()
                mw.move(y+1, 0)
            elif c == 'l':
                ch.display_list_view(mw)
            elif c == 'p':
                stdscr.refresh()
                mw.refresh()
        # otherwise do some background things (update clock, etc)
        except curses.error:
            (cY, cX) = mw.getyx()
            ch.display_time(stdscr)
            if (not elm.is_connected()):
                elm.connect()
            t1 = time.time()
            if (t1 - t0 > dt):
                t0 = t1
                mw.clear()
                ch.display_list_view(mw)
            ch.display_status(stdscr)
            mw.move(cY, cX)

        #stdscr.refresh()
        mw.refresh()
        

curses.wrapper(main)
