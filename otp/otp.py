import argparse
import sys
import base64
import threading
import SocketServer
import signal
import time
from log import set_logging_level, log, levels

# Globals
BLOCKSIZE = 512
FLAG = 'acsc2017{depth_defeats_all}'


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='OTP - The only unbreakable encryption')
    parser.add_argument('-p', '--port', action='store', dest='port', required=False, default=31337, type=int,
                        help='The port to serve the OTP challenge on.')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', required=False, default=False,
                        help='Enable debug messages')

    return parser.parse_args()


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def intro(self, request):
        log('Serving intro', levels.DEBUG)
        prompt = "OTP - The only unbreakable encryption (google it!)" \
        "\nWe're so confident in this encryption, we'll take any string you send, and return it along with the flag!" \
        "\nGood luck trying to break unbreakable encryption!" \
        "\nEnter your string: "
        request.sendall(prompt)
        data = request.recv(1024).strip()
        cur_thread = threading.current_thread()
        client_message = "{}: {}".format(cur_thread.name, data)
        log(client_message, levels.INFO)
        this_key = self.get_key()
        encrypted_string = self.encrypt(data, this_key)
        request.sendall('{}\n'.format(encrypted_string))

    def get_key(self):
        '''
        Get a key from /dev/urandom, unbreakable!
        :return: a random key
        '''
        with open('/dev/urandom' ,'rb') as urandom_file:
            key = urandom_file.read(BLOCKSIZE)
        log('Key: {}'.format(repr(key)), levels.DEBUG)
        return key

    def encrypt(self, message, key):
        '''
        Encrypt a message with a key
        :param message: User supplied message (string)
        :param key: Random OTP key (bytes)
        :return: encrypted string (base64 string)
        '''
        message_and_flag = '{} {}'.format(message, FLAG)
        encrypted_bytes = ''
        for index, letter in enumerate(message_and_flag):
            if index >= BLOCKSIZE:
                index -= BLOCKSIZE
            log('Encrypting {} with {}'.format(letter, repr(key[index])), levels.DEBUG)
            encrypted_bytes += chr(ord(letter) ^ ord(key[index]))
            log('Encrypted byte: {}'.format(repr(encrypted_bytes[-1])), levels.DEBUG)
        return base64.b64encode(encrypted_bytes)



    def handle(self):
        self.intro(self.request)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass



class otp(object):

    def __init__(self, port):
        '''
        Standard setup. Defined the port to listen on
        :param port: int, port number to listen on
        '''
        self.port = port
        self.server = None


    def main(self):
        self.server = ThreadedTCPServer(('0.0.0.0', self.port), ThreadedTCPRequestHandler)
        ip, port = self.server.server_address
        log('Set up server on {} and port {}'.format(ip, port), levels.PLUS)
        #self.server.serve_forever()

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        log("Server loop running in thread: {}".format(server_thread.name), levels.PLUS)
        # A really sloppy way to ensure we can catch a control+c
        while True:
            time.sleep(.1)

    def stop(self):
        log('Shutting down serve_forever()', levels.DEBUG)
        self.server.shutdown()
        log('serve_forever() shut down', levels.DEBUG)
        self.server.server_close()

def main():
    # Catch all Control+C's
    def handler(signum, frame):
        log('Signal handler called with signal {}'.format(signum), levels.DEBUG)
        log('Shutting down', levels.WARNING)
        if my_otp is not None:
            my_otp.stop()
        log('Finished stopping', levels.DEBUG)
        sys.exit(0)

    # Register the handler for Ctl+C
    signal.signal(signal.SIGINT, handler)

    args = parse_args(sys.argv)
    if args.verbose:
        set_logging_level(levels.DEBUG)
    else:
        set_logging_level(levels.INFO)

    my_otp = otp(args.port)
    my_otp.main()






if __name__ == '__main__':
    main()
