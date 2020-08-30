https://gist.github.com/zhuker/8d5c8febf85d41e248687ed732e92ddb
while true; do xinput test-xi2 --root | ./globalinput.py  | nc pi-zero-w 4000; done
