#! /usr/env/bin python2.6
# -*- coding: utf-8 -*-
"""
    client

    description

    @copyright: 2010 DiogenesAugusto <diofeher@gmail.com>
    @license: see LICENSE.
"""
import settings
from socket import socket, AF_INET, SOCK_STREAM

client = socket(AF_INET, SOCK_STREAM)
client.connect((settings.HOST, settings.PORT))
client.send('bolas')
data = client.recv(1024)
print data

#TODO Craete QT Widgets