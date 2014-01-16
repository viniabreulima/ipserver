#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
IPSERVER
'''

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urlparse
import json
import datetime

class Handler(BaseHTTPRequestHandler):
    clients = {}

    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(401)
            return
            
        client_ip = self.client_address[0]
        get_data = {}
        if '?' in self.path:
            qs = self.path.split('?', 1)[-1]
            get_data = dict(urlparse.parse_qsl(qs))

        result = 'Hello ' + client_ip

        if get_data.get('list') == 'yep':
            result += '\n\nHere is the client list:'
            result += json.dumps(self.clients, indent=2, sort_keys=True)
        else:
            self.clients[client_ip] = get_data.get('name', '---') + '|' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
        self.send_response(200)
        self.send_header('content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(result)


def run(port=8000):
    '''
    Starts server
    '''
    server_address = ('', port)
    httpd = HTTPServer(server_address, Handler)
    print 'Starting server on port %d' % port
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        print 'Bye bye!'


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', '-p', default=8000)
    args = ap.parse_args()

    run(args.port)
