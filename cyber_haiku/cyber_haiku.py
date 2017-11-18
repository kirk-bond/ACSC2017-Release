#!/usr/bin/env python2

import argparse
import sys
import random
import threading
import SocketServer
import signal
import time
from log import set_logging_level, log, levels

GLOBALS = {
    'FLAG':'acsc2017{user_input_is_evil}',
    'FIVE': ['packets were flying\n', 'fingers on the keys\n', 'always default drop\n', 'mechanical keys\n'],
    'SEVEN': ['all around us, there were bits\n', 'firewalls blocking all bits\n', 'no hope for a stray PSH ACK\n', 'fire the cyber bullets\n'],
}

def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Cyber Haiku Generator 9000')
    parser.add_argument('-p', '--port', action='store', dest='port', required=False, default=5000, type=int,
                        help='The port to serve the Cyber Haiku challenge on.')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', required=False, default=False,
                        help='Enable debug messages')

    return parser.parse_args()

class Data(object):
    def __init__(self, object_type, length, content):
        self.object_type = object_type
        self.length = length
        self.content = content


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def intro(self, request):
        log('Serving intro', levels.DEBUG)
        prompt = "Cyber Haiku Generator 9000" \
        "\nNumber of Haiku's to generate: "
        request.sendall(prompt)
        raw_data = request.recv(1024).strip()
        this_data = Data(type(raw_data), len(raw_data), raw_data)
        cur_thread = threading.current_thread()
        client_message = "{}: {}".format(cur_thread.name, this_data.content)
        log(client_message, levels.INFO)
        format_string = "Here are your {} Haiku's\n\n".format(this_data.content)
        log(format_string, levels.DEBUG)
        response = format_string.format(data=this_data)
        log(response, levels.DEBUG)
        try:
            num = int(this_data.content)
        except Exception as e:
            log('Invalid number supplied by user', levels.WARNING)
            log(e, levels.WARNING)
            num = 1
        for x in range(num):
            response += self.generate_haiku()
            response += '\n'
        request.sendall(response)

    def generate_haiku(self):
        return random.choice(GLOBALS['FIVE']) + random.choice(GLOBALS['SEVEN']) + random.choice(GLOBALS['FIVE'])

    def handle(self):
        self.intro(self.request)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass



class cyber_haiku(object):

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
        log('Shutting down server_forever()', levels.DEBUG)
        self.server.shutdown()
        log('server_forever() shut down', levels.DEBUG)
        self.server.server_close()

def main():
    # Catch all Control+C's
    def handler(signum, frame):
        log('Signal handler called with signal {}'.format(signum), levels.DEBUG)
        log('Shutting down', levels.WARNING)
        if my_cyber_haiku is not None:
            my_cyber_haiku.stop()
        log('Finished stopping', levels.DEBUG)
        sys.exit(0)

    # Register the handler for Ctl+C
    signal.signal(signal.SIGINT, handler)

    args = parse_args(sys.argv)
    if args.verbose:
        set_logging_level(levels.DEBUG)
    else:
        set_logging_level(levels.INFO)

    my_cyber_haiku = cyber_haiku(args.port)
    my_cyber_haiku.main()



if __name__ == '__main__':
    main()
