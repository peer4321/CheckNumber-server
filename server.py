#!/usr/bin/python

import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from handler import browse_handler, months_handler, addnew_handler, delete_handler, result_handler

host = '0.0.0.0'
port = 5000

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = {}
        path = self.path
        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)
        print path, qs
        if path == '/browse.xml':
            browse_handler(self, path, qs)
        if path == '/months.xml':
            months_handler(self, path, qs)
        if path == '/result.xml':
            result_handler(self, path, qs)

    def do_POST(self):
        if self.path == '/submit':
            addnew_handler(self)
        if self.path == '/delete.xml':
            delete_handler(self)

    def log_request(self, code = None, size = None):
        print 'Request'

    def log_message(self, format, *args):
        print 'Message'

if __name__ == "__main__":
    try:
        server = HTTPServer((host, port), MyHandler)
        print 'Started HTTP Server'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

