#!/usr/bin/env python3
# A web server to echo back a request's headers and data.
#
# Usage: ./webserver
#        ./webserver 0.0.0.0:5000

from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import argv
import numpy as np

BIND_HOST = 'localhost'
PORT = 8008

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.write_response(bytes("ECHO", "utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_length)
        if(str(body) == "b'getOrders'"):
            with open('orders.txt') as f:
                body = f.read()
            body = body.splitlines()
            print(body)
            np.random.shuffle(body)
            body = body[0]
        elif((str(body)).find("DONE") >= 0):
            print((str(body)[2:-6]))
            print('Done - ' + str(body)[2:-6])
        else:
            print('error')
            body = 'ERROR'

        self.write_response(bytes(str(body), "utf-8"))

    def write_response(self, content):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(content)

        #print(self.headers)
        #print(content.decode('utf-8'))


if len(argv) > 1:
    arg = argv[1].split(':')
    BIND_HOST = arg[0]
    PORT = int(arg[1])

print(f'Listening on http://{BIND_HOST}:{PORT}\n')

httpd = HTTPServer((BIND_HOST, PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()