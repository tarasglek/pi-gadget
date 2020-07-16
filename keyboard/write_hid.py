#!/usr/bin/env python3
import sys

NULL_CHAR = chr(0)
# https://randomnerdtutorials.com/raspberry-pi-zero-usb-keyboard-hid/
# https://stackoverflow.com/questions/22753160/how-do-i-accept-input-from-arrow-keys-or-accept-directional-input
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())
# 1 is on the right
# [Right Meta | Right Alt | Right Shift | Right Control | Left Meta | Left Alt | Left Shift | Left Control]
CTRL = 0x1
SHIFT = 0x2
ALT = 0x4
"""
https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf
"""
def type_key(expression, fd):
    modifier = 0
    parts = expression.split('+')
    remaining = []
    out = chr(0)
    for part in parts:
        if part == "SHIFT":
            modifier = modifier | SHIFT
        elif part == "CTRL":
            modifier = modifier | CTRL
        elif part == "ALT":
            modifier = modifier | ALT
        else:
            remaining.append(part)
    letter = lambda c: chr(ord(c) - ord('a') + 4)
    table = {
        '0': 39,
        ' ': 44,
        'SPACE': 44,
        'RETURN': 40,
        'ESC': 41,
        'BACKSPACE': 42,
        'TAB': 43,
        '-':45,
        'F1': 58,
        'F2': 59,
        'F4': 61,
        'F12': 69,
        'DELETE': 76,
        'RIGHT': 79,
        'LEFT': 80,
        'DOWN': 81,
        'UP': 82,
    }
    if len(remaining):
        key = remaining[0]
        if key in table:
            out = chr(table[key])
        elif key >= 'a' and key <= 'z':
            # 4 == 'a' in usb hid table
            out = letter(key.lower())
        elif key >= '1' and key <= '9':
            out = chr(ord(key) - ord('1') + 30)
        else:
            print("Unhandled key:" + repr(key), file=sys.stderr)
    out = chr(modifier << 4) + NULL_CHAR + out + NULL_CHAR*5
    out += NULL_CHAR*8
    fd.write(out.encode())

def typeit(str):
    with open('/dev/hidg0', 'rb+') as fd:
        [type_key(c, fd) for c in str]
        for word in ["\r", "BACKSPACE","ESC",  "F12", "TAB", "UP", "DOWN", "LEFT", "RIGHT"]:
            type_key(word, fd)
    # write_report(NULL_CHAR*8)
        # type_key(None, fd)

for line in sys.stdin:
    with open('/dev/hidg0', 'rb+') as fd:
        type_key(line.rstrip(), fd)
