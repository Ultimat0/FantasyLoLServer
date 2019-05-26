# -*- coding: utf-8 -*-
"""
Created on Sun May 26 15:22:07 2019

@author: markn
"""

import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()