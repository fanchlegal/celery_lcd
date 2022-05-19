# coding: utf-8

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("", 1111))

s.send(b'Hello world')
