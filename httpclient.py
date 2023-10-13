#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    
    def connect(self, host, port=80):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        try:
            return int(data.split(' ')[1])
        except:
            return None

    def get_headers(self, data):
        return data.split('\r\n\r\n')[0]

    def get_body(self, data):
        return data.split('\r\n\r\n')[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if part:
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8', errors='ignore')

    def GET(self, url, args=None):
       parsed_url = urllib.parse.urlparse(url)
       self.connect(parsed_url.hostname, parsed_url.port)#connecting to the server
       request_line = f"GET {parsed_url.path} HTTP/1.1\r\n"#building http request
       headers = f"Host: {parsed_url.hostname}\r\n\r\n"
       self.sendall(request_line + headers)#sending the request
       response_data = self.recvall(self.socket)#recieving the request
       code = self.get_code(response_data)#assigning response to code and body
       body = self.get_body(response_data)
       self.close()
       return HTTPResponse(code, body)

  


    

    def POST(self, url, args=None):
        parsed_url = urllib.parse.urlparse(url)
    
        self.connect(parsed_url.hostname, parsed_url.port)#tcp connection with server
        
        content_type = "application/x-www-form-urlencoded"#default for submitting post
        body = ""
        if args is not None:
            body = urllib.parse.urlencode(args)#converts to ASCII string 
        
        content_length = len(body)
        
        request_line = f"POST {parsed_url.path} HTTP/1.1\r\n"#building http request
        headers = f"Host: {parsed_url.hostname}\r\n"
        headers += f"Content-Type: {content_type}\r\n"
        headers += f"Content-Length: {content_length}\r\n\r\n"
        
        self.sendall(request_line + headers + body)#sent to server
        response_data = self.recvall(self.socket)#recieve the code from server
        
        code = self.get_code(response_data)
        body = self.get_body(response_data)
        
        self.close()#close connection
        return HTTPResponse(code, body)


    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST(url, args)
        else:
            return self.GET(url, args)

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command(sys.argv[2], sys.argv[1]))
    else:
        print(client.command(sys.argv[1]))