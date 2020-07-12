#!/usr/bin/env python3
import click
import sys

def click2code(c):
    table = {
        '\x1b[A': "UP",
        '\x1b[B': "DOWN",
        '\x1b[C': "RIGHT",
        '\x1b[D': "LEFT",
        '\x7f': "BACKSPACE",
        '\x1bOP': 'F1',
        '\x1bOQ': 'F2',
        '\x1b[24~': 'F12',
    }
    if c in table:
        return table[c]
    elif len(c) == 1:
        return c
    return repr(c)

while True:
    c = click.getchar()
    code = click2code(c)
    print(code)
    # debug output
    print("Pressed (%s, %s)" % (code, repr(c)),file=sys.stderr)