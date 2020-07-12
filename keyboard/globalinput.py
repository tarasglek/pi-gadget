#!/usr/bin/env python3
# keymap xmodmap -pke
# xinput test-xi2 --root
import sys
import subprocess

def parse_keys():
    s = subprocess.check_output("xmodmap -pke", shell=True).decode("utf-8").rstrip()
    ret = {}
    for line in s.split("\n"):
        pieces = line.split()
        if len(pieces) >= 4:
            ret[pieces[1]] = pieces[3]
    return ret

keymap = parse_keys()
CTRL = 0x4
ALT = 0x8
SHIFT = 0x1

def parse_event(e):
    lines = e.split("\n")
    header = lines.pop(0).split(' ')
    if not '(KeyPress)' in header:
        return
    key = None
    modifiers = []
    for line in lines:
        stuff = line.strip().split(': ', 1)
        # print(stuff)
        if stuff[0] == 'detail':
            key = keymap[stuff[1]]
            print(key)
        elif stuff[0] == 'modifiers':
            modifier_mask = int(stuff[1].split().pop(), 16)
            if modifier_mask & SHIFT:
                modifiers.append("SHIFT")
            if modifier_mask & CTRL:
                modifiers.append("CTRL")
            if modifier_mask & ALT:
                modifiers.append("ALT")
    ret = '+'.join(modifiers + [key])
    print(ret)
        # print(stuff)

def parse_input():
    payload = ''
    for line in sys.stdin:
        line = line.rstrip()
        # print(repr(line))
        if line == '' or line[0] != ' ':
            if len(payload):
                if payload[:5] == "EVENT":
                    parse_event(payload.rstrip())
                payload = ''
            if line == '':
                continue
        payload += line + "\n"
        # print(line)
parse_input()