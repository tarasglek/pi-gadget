#!/usr/bin/env python3
import sys

NULL_CHAR = chr(0)
# https://randomnerdtutorials.com/raspberry-pi-zero-usb-keyboard-hid/
# https://stackoverflow.com/questions/22753160/how-do-i-accept-input-from-arrow-keys-or-accept-directional-input
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())
"""
https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf
"""
def type_key(key, fd):
    letter = lambda c: chr(ord(c) - ord('a') + 4) + NULL_CHAR * 5
    table = {
        '0': 39,
        ' ': 44,
        '\r': 40,
        'ESC': 41,
        'BACKSPACE': 42,
        '\t': 43,
        '-':45,
        'F1': 58,
        'F2': 59,
        'F12': 69,
        'RIGHT': 79,
        'LEFT': 80,
        'DOWN': 81,
        'UP': 82,
    }
    if key in table:
        out = NULL_CHAR*2+chr(table[key])+NULL_CHAR*5
    elif key >= 'a' and key <= 'z':
        # 4 == 'a' in usb hid table
        out = NULL_CHAR*2 + letter(key)
    elif key >= 'A' and key <= 'Z':
        # 4 == 'a' in usb hid table
        out = chr(32)+NULL_CHAR + letter(key.lower())
    elif key >= '1' and key <= '9':
        # 4 == 'a' in usb hid table
        out = NULL_CHAR*2 +chr(ord(c) - ord('1') + 30) + NULL_CHAR * 5
    else:
        print("Unhandled key:" + repr(key))
        return
    # Release all keys
    print(len(out))
    out+=(NULL_CHAR*8)
    fd.write(out.encode())

def typeit(str):
    with open('/dev/hidg0', 'rb+') as fd:
        [type_key(c, fd) for c in str]
        for word in ["\r", "BACKSPACE","ESC",  "F12", "\t", "UP", "DOWN", "LEFT", "RIGHT"]:
            type_key(word, fd)
    # write_report(NULL_CHAR*8)
        # type_key(None, fd)

for line in sys.stdin:
    print("foo:" + line.rstrip())