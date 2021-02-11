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

    '''
    helper function return, the host name and port number, path
    '''
    def get_host_port_path(self, url):
        # we can use cppy.deepcoy ?
        o = urllib.parse.urlparse(url)
        if o.port == None:
            port = 80
        else :
            port = o.port

        path = o.path
        if path == "":
          path = "/"

        print(o)
        return o.hostname, port, path

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        split_array = data.split('\r\n\r\n')
        protocal_status_info = split_array[0].split()

        return int(protocal_status_info[1])

    # helper funciton, design for build body for content
    def build_send_body(self, args):
        send_body = ""
        if args != None:
            last_key = list(args)[-1]
            for key, value in args.items():
                if key != last_key:
                    send_body = send_body + key + "=" + value + "&"
                else:
                    send_body = send_body + key + "=" + value

        return send_body
        
    def get_body(self, data):
        return data.split('\r\n\r\n', 1)[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        print("data sent successfully")
        
    def close(self):
        self.socket.close()
        print("socket shut down")

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')


    def GET(self, url, args=None):

        code = 500
        body = ""

        host, port, path = self.get_host_port_path(url)
        # connect to the host
        self.connect(host, port)
        message = "GET " + path +" HTTP/1.1\r\n"
        message = message + "Host: " + host + "\r\nConnection: close\r\n\r\n" # headers end ,body end 

        self.sendall(message)
        data = self.recvall(self.socket)

        print(" - Response data -")
        print(data)
        print ("-- Response data --")

        code = self.get_code(data)
        body = self.get_body(data)


        # close before we exit 
        self.close() 

        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        host, port, path = self.get_host_port_path(url)
        # connect to the host
        self.connect(host, port)

        send_body = self.build_send_body(args)

        message = "POST " + path +" HTTP/1.1\r\n"       
        message = message + "Host: " + host + "\r\nConnection: close\r\n" + "Content-Type: application/x-www-form-urlencoded\r\n"
        message = message + "Content-Length: " + str(len(send_body)) + "\r\n\r\n" #head end
        message = message + send_body  #body end

        self.sendall(message)
        data = self.recvall(self.socket)

        print(" - Response data -")
        print(data)
        print ("-- Response data --")
        code = self.get_code(data)
        body = self.get_body(data)

        # close before we exit 
        self.close() 
        return HTTPResponse(code, body)


    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
