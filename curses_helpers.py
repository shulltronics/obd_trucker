import time
import curses
### Global Variables ###
from settings import *
from PIDs import *

# return the x-coordinate that string should start at
# in order to be justified within dx characters
def get_justified_startx(dx, string, justification = "LEFT"):
    if justification == "LEFT":
        return 0
    elif justification == "CENTER":
        return int((dx - len(string)) / 2)
    elif justification == "RIGHT":
        return (int(dx - len(string)))

def display_legend(win):
    desc_lens = []
    for key, desc in key_options.items():
        desc_lens.append(len(desc))
    desc_lens.sort()
    max_desc_len = desc_lens[len(desc_lens) - 1]
    for key, desc in key_options.items():
        (y, x) = win.getyx()
        win.addstr(y + 2, int((curses.COLS - (max_desc_len + 2*gMENU_PADDING)) / 2),
                   key + ' - ' + desc)
    win.move(y + 2, 0)

def display_time(win):
    t = time.asctime()
    (cY, cX) = win.getyx()
    (_, dx) = win.getmaxyx()
    timeX = get_justified_startx(dx, t, "RIGHT") - 2
    win.addstr(1, timeX, t)

def display_status(win):
    win.move(1, 2)
    if elm.is_connected():
        win.addch(curses.ACS_BLOCK, curses.color_pair(2))
        win.addstr(" Connected", curses.color_pair(2))
    else:
        win.addch(curses.ACS_BLOCK, curses.color_pair(1))
        win.addstr(" Disconnected", curses.color_pair(1))
    win.hline(" ", 20)
    

def display_header(win):
    win.clear()
    win.border()
    header = "  " + gPROG_NAME + " " + "v" + gVERSION + "  "
    (cY, cX) = win.getyx()
    (_, dX) = win.getmaxyx()
    win.addstr(0, get_justified_startx(dX, header, "CENTER"),
               header, curses.A_BOLD)
    display_time(win)
    display_status(win)
    win.move(2, 0)
    win.addch(curses.ACS_LTEE)
    win.hline(curses.ACS_HLINE, curses.COLS - 2)
    win.addch(2, curses.COLS - 1, curses.ACS_RTEE)

def display_list_view(win):
    (my, mx) = win.getmaxyx()
    (cy, cx) = win.getyx()
    # remember the row for adding data labels after
    # PID, names, etc have been parsed and lengths obtained
    label_y = cy

    # some variables for pretty-printing
    highlight = True
    pid_max_len = 0
    name_max_len = 0

    cy += 2
    win.move(cy, cx)

    # find max string lengths
    for m in PIDs:
        (name, pid) = (m[0], m[2])
        name_max_len = max(name_max_len, len(name))
        pid_max_len  = max(pid_max_len , len(hex(pid)))

    pid_x  = 1
    name_x = pid_x + pid_max_len + 2
    val_x  = name_x + name_max_len + 2
 
    for m in PIDs:
        (name, pid) = (m[0], m[2])
        win.addstr(hex(pid) + " ")
        win.addch(curses.ACS_VLINE)
        win.move(cy, name_x)
        win.addstr(str(name) + " ")
        win.move(cy, val_x - 1)
        win.addch(curses.ACS_VLINE)
        cy = cy + 1
        win.move(cy, 0)

    dx = get_justified_startx(pid_max_len, "PID", "CENTER")
    win.move(label_y, dx)
    win.addstr("PID", curses.A_BOLD | curses.A_UNDERLINE)
    win.move(label_y, name_x - 2)
    win.addch(curses.ACS_VLINE)
    win.addch(" ")
    (_, cx) = win.getyx()

    dx = get_justified_startx(name_max_len, "Name", "CENTER")
    win.addstr(label_y, name_x + dx, "Name", curses.A_BOLD | curses.A_UNDERLINE)
    win.move(label_y, val_x - 1)
    win.addch(curses.ACS_VLINE)
    win.addch(" ")

    win.addstr("Value", curses.A_BOLD | curses.A_UNDERLINE)

    win.refresh()

    # aquire and print the values
    (cy, cx) = win.getyx()
    cy += 2
    win.move(cy, val_x)
    for m in PIDs:
        pid = m[2]
        r = elm.request_pid(pid)
        win.addstr(" " + r)
        if (r != "Error"):
            v = str(m[6](r.split()))
            win.addstr(" " + v)
        win.refresh()
        cy = cy + 1
        win.move(cy, val_x)

    cy = cy + 1
    win.move(cy, 0)
