#!/usr/bin/env python2

import base64
from pwn import *

#context.log_level = "debug"

def xor(s1, s2):
    return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

conn = remote("localhost", 5000)
conn.recvuntil("Enter your string: ")
conn.send("\x00"*512)

ct = base64.b64decode(conn.recvall())
keystream = ct[:512]
flag_ct = ct[512:]
flag = xor(keystream, flag_ct)
log.success("Flag: " + flag)
