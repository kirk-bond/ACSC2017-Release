#!/usr/bin/env python3

import socket

def recvline(s):
    nl = "\n".encode("utf8")
    while s.recv(1) != nl:
        pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 5000))
recvline(s)
recvline(s)

while (True):
    try:
        # Receive
        expr = s.recv(32).decode("utf8")
        expr = expr.strip()
        print(expr)

        # Sanitize
        expr = expr.replace("x", "*")
        expr = expr.replace("/", "//")  # python3

        # Solve and submit
        soln = str(eval(expr)) + "\n"
        s.send(soln.encode("utf8"))
        recvline(s)
    except:
        break
