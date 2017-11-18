import base64
from pwn import *

SERVER = '127.0.0.1'
PORT = 31337

# Connect to the socket
connection = remote(SERVER, PORT)
# Get the intro text
connection.recvuntil('Enter your string: ')
# Send 512 bytes of A's
print "Sending 512 A's"
connection.send('A'*512)
# Get the encrypted string
print 'Receiving base64 string'
base64_string = connection.recv(2048)
connection.close()
print 'Base64 string: {}'.format(base64_string)
encrypted_data = base64.b64decode(base64_string)
print 'Raw encrypted data: {}'.format(repr(encrypted_data))
key = ''
for index, byte in enumerate(encrypted_data):
    if index == 511: # This is the weakness! Key reuse makes OTP worthless, especially when we control the plaintext
        break
    key += chr(ord('A') ^ ord(encrypted_data[index]))
print '\nKey: {}'.format(repr(key))
flag_data = encrypted_data[512:]
flag = ''
for index, bytes in enumerate(flag_data):
    flag += chr(ord(key[index]) ^ ord(flag_data[index]))
print '\nFlag: {}'.format(flag)
