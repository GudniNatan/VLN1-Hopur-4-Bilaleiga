import os
import sys

KEYMAP = {
    10: 13,
    127: 8,
    10051: 10083,
    10065: 10072,
    10066: 10080,
    10067: 10077,
    10068: 10075
}


def readkey():
    if os.name == 'nt':
        from msvcrt import getwch
        key = ord(getwch())
        if key == 224:
            key = ord(getwch()) + 10000
        return key
    else:
        return readkey_unix()


def readkey_unix():
    import termios, fcntl
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
    try:
        while 1:
            try:
                c = ord(sys.stdin.read(1))
                if c == 27:
                    sys.stdin.read(1)
                    c = ord(sys.stdin.read(1)) + 10000
                break
            except IOError:
                pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    return KEYMAP.get(c, c)
