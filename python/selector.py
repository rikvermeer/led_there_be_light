class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
    
import time
from generators import *
from ledcontroller import *
from fragmentcontroller import *

key = range(0, 260)
f_key = Fragment(len(key), key)

colors = [[0, 0, 255], [0,255,0], [255,0,0]]
getch = _Getch()
g_key = ThreadedGenerator(0.01, f_key)
g_key.start = 0
g_key.end = 0
g_key.done = []
def write_key():
    c = ord(getch.__call__())
    changed = False
    if c == 224:
        c = ord(getch.__call__())
    if c == 72:
        pass
    elif c == 80:
        pass
    elif c == 75:
        g_key.end -= 1
        changed = True
    elif c == 77:
        changed = True
        g_key.end += 1
    elif chr(c).isspace():
        changed = True
        g_key.done.append([g_key.start, g_key.end])
        g_key.start = g_key.end
    if changed:
        g_key.end = sanitize(g_key.end)
        
        for index, value in enumerate(g_key.done):
            color = colors[index]
            for i in range(value[0], value[1]):
                for index, value in enumerate(color):
                    g_key.fragment.data[i * 3 + index] = value
        
        g_key.fragment.data[g_key.start * 3 + 1] = 255
        g_key.fragment.data[g_key.stop * 3] = 255
    
def sanitize(pos):
    if pos < 0:
        pos = 0
    if pos > g_key.fragment.size -1:
        pos = g_key.fragment.size -1
    return pos
    
fc = FragmentController()
fc.addFragment(f_key)
g_key.start()
fc.start()