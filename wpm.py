import curses
from curses import wrapper
import time
import random


def start(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Typing Test!")
    stdscr.addstr("\nPress any key to begin")
    stdscr.refresh()
    stdscr.getkey()

def display(stdscr,target,current,wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0 ,f"WPM: {wpm}")

    for i,ch in enumerate(current):
        correct = target[i]
        color = curses.color_pair(1)
        if ch != correct:
            color = curses.color_pair(2)

        stdscr.addstr(0, i , ch , color)

def load():
    with open(r"C:\Users\Pramath\Documents\python\Typing Test\text.txt", "r") as f:
        lines = f.readlines()

        return random.choice(lines).strip()

def test(stdscr):
    target = load()
    current = []
    wpm = 0

    start_t = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapse = max(time.time() - start_t, 1)
        wpm = round((len(current) / (time_elapse / 60)) / 5)

        stdscr.clear()
        display(stdscr, target, current, wpm)
        stdscr.refresh()

        if "".join(current) == target:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current) > 0:
                current.pop()
        elif len(current) < len(target):
            current.append(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start(stdscr)
    while True:

        test(stdscr)

        stdscr.addstr(2, 0, "You completed the test! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break 

wrapper(main)
