#!/usr/bin/env python3

import click

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
        ' ': 44,
        'ENTER': 40,
        'ESC': 41,
        'BACKSPACE': 42,
        'TAB': 43,
        'F12': 69,
        'RIGHT': 79,
        'LEFT': 80,
        'DOWN': 81,
        'UP': 82
    }
    if key in table:
        out = NULL_CHAR*2+chr(table[key])+NULL_CHAR*5
    elif key >= 'a' and key <= 'z':
        # 4 == 'a' in usb hid table
        out = NULL_CHAR*2 + letter(key)
    elif key >= 'A' and key <= 'Z':
        # 4 == 'a' in usb hid table
        out = chr(32)+NULL_CHAR + letter(key.lower())
    else:
        raise Exception("Unhandled key:" + key)
    # Release all keys
    out+=(NULL_CHAR*8)
    fd.write(out.encode())

def typeit(str):
    with open('/dev/hidg0', 'rb+') as fd:
        [type_key(c, fd) for c in str]
        for word in ["ENTER", "BACKSPACE","ESC",  "F12", "TAB", "UP", "DOWN", "LEFT", "RIGHT"]:
            type_key(word, fd)
    # write_report(NULL_CHAR*8)
        # type_key(None, fd)
printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

while True:
    c = click.getchar()
    click.echo()
    if c == 'y':
        click.echo('We will go on')
    elif c == 'n':
        click.echo('Abort!')
        break
    elif c == '\x1b[D':
        click.echo('Left arrow <-')
    elif c == '\x1b[C':
        click.echo('Right arrow ->')
    else:
        click.echo(repr([c, ord(c)]))
        click.echo('You pressed: "' + ''.join([ '\\'+hex(ord(i))[1:] if i not in printable else i for i in c ]) +'"' )