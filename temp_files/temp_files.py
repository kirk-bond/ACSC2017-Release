#!/usr/bin/env python2

import argparse
import sys
import tempfile
import threading
import SocketServer
import signal
import pyinotify
import os
import shutil
import subprocess
import glob
import time
from log import set_logging_level, log, levels

# Globals
TEMP_DIR = '/home/user/temp_files'
MAX_TEMP_FILES = 5000
CURRENT_TEMP_FILES = 0
MAX_TEMP_AGE = 1 # in minutes
SLEEP_SECONDS = 30


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Simple File Storage')
    parser.add_argument('-p', '--port', action='store', dest='port', required=False, default=5000, type=int,
                        help='The port to serve the python interpreter on.')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', required=False, default=False,
                        help='Enable debug messages')

    return parser.parse_args()


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def main_menu(self, request):
        log('Serving main menu', levels.DEBUG)
        prompt = '\nSimple File Manager\n[0] Read a file\n' \
        '[1] Write a file\n[2] List files\n[3] Display Python version\nEnter your choice: '
        request.sendall(prompt)
        data = request.recv(1024).strip()
        cur_thread = threading.current_thread()
        debug_msg = "{}: {}".format(cur_thread.name, data)
        log(debug_msg, levels.DEBUG)
        if data not in ['0', '1', '2', '3']:
            response = 'Pick an option next time\n'
            request.sendall(response)
        else:
            self.handle_choice(data, request)

    def handle_choice(self, choice, request):
        if choice == '0':
            prompt = 'Enter the filename: '
            request.sendall(prompt)
            data = request.recv(1024).strip()
            data = data.replace('.','').replace('/', '')
            path = '{}/{}'.format(self.tempdir, data)
            if os.path.exists(path):
                with open(path, 'r') as read_file:
                    response = '{} contains:\n'.format(path)
                    response += '\n'.join(read_file.readlines())
            else:
                response = '{} not found\n'.format(path)
            request.sendall(response)
            self.main_menu(request)
        elif choice == '1':
            if CURRENT_TEMP_FILES >= MAX_TEMP_FILES:
                response = 'Too many temp files\n'
                request.sendall(response)
                return
            prompt = 'Enter the file name: '
            request.sendall(prompt)
            file_name = request.recv(1024).strip()
            file_name = file_name.replace('.', '').replace('/','')
            response = 'Enter the file contents: '
            request.sendall(response)
            file_contents = request.recv(1024)
            log('Got file name {} and contents {}'.format(file_name, file_contents), levels.DEBUG)
            path = '{}/{}'.format(self.tempdir, file_name)
            with open(path, 'w') as write_file:
                write_file.write(file_contents)
            response = '{} written\n'.format(path)
            request.sendall(response)
            self.main_menu(request)
        elif choice == '2':
            all_files = [files for files in glob.glob('{}/*'.format(self.tempdir))]
            response = '\n'.join(all_files)
            response += '\n'
            request.sendall(response)
            self.main_menu(request)
        elif choice == '3':
            command_file = tempfile.mktemp(prefix='tmp', suffix='file', dir=self.tempdir)
            log('Writing to {}'.format(command_file), levels.DEBUG)
            with open(command_file, 'w') as command_file_obj:
                command_file_obj.write('python -V')
            response = 'Waiting {} seconds to prevent DoS\n'.format(SLEEP_SECONDS)
            request.sendall(response)
            time.sleep(SLEEP_SECONDS)
            with open(command_file, 'r') as command_file_obj:
                command = ''.join(command_file_obj.readlines())
            log('Executing: {}'.format(command), levels.DEBUG)
            response = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            request.sendall('Result:\n{}'.format(response))
            os.remove(command_file)
            self.main_menu(request)

    def handle(self):
        prompt = 'Enter a hard to guess subdirectory name to use for your files: '
        self.request.sendall(prompt)
        dir_name = self.request.recv(1024).strip()
        dir_name = dir_name.replace('.', '').replace('/', '')
        self.tempdir = '{}/{}'.format(TEMP_DIR, dir_name)
        if not os.path.exists(self.tempdir):
            os.makedirs(self.tempdir)

        self.main_menu(self.request)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        global  CURRENT_TEMP_FILES
        clean_temp_files()
        log('New file created: {}'.format(event.pathname), levels.ASTERISK)
        CURRENT_TEMP_FILES += 1

    def process_IN_DELETE(self, event):
        global CURRENT_TEMP_FILES
        log('File removed: {}'.format(event.pathname), levels.ASTERISK)
        CURRENT_TEMP_FILES -= 1

def clean_temp_files():
    for files in glob.glob('{}/*'.format(TEMP_DIR)):
        log('Checking file {}'.format(files), levels.DEBUG)
        log(os.path.getmtime(files), levels.DEBUG)
        if int(time.time()) - int(os.path.getmtime(files)) > (60*MAX_TEMP_AGE):
            os.remove(files)
            log('Removed {} due to age'.format(files), levels.DEBUG)



class file_manager(object):

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

        # Monitor temp files
        if not os.path.exists(TEMP_DIR):
            os.mkdir(TEMP_DIR)
        watch_manager = pyinotify.WatchManager()
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events
        self.notifier = pyinotify.Notifier(watch_manager, EventHandler())
        watch_manager.add_watch(TEMP_DIR, mask, rec=True)
        log('Watching {} for changes'.format(TEMP_DIR), levels.PLUS)
        self.notifier.loop()

    def stop(self):
        log('Shutting down server_forever()', levels.DEBUG)
        self.server.shutdown()
        log('server_forever() shut down', levels.DEBUG)
        self.server.server_close()
        self.notifier.stop()
        shutil.rmtree(TEMP_DIR)

def main():
    # Catch all Control+C's
    def handler(signum, frame):
        log('Signal handler called with signal {}'.format(signum), levels.DEBUG)
        log('Shutting down', levels.WARNING)
        if my_file_manager is not None:
            my_file_manager.stop()
        log('Finished stopping', levels.DEBUG)
        os._exit(0)
        sys.exit(0)

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    # Register the handler for Ctl+C
    signal.signal(signal.SIGINT, handler)

    args = parse_args(sys.argv)
    if args.verbose:
        set_logging_level(levels.DEBUG)
    else:
        set_logging_level(levels.INFO)

    my_file_manager = file_manager(args.port)
    my_file_manager.main()






if __name__ == '__main__':
    main()
