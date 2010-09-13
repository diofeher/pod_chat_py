#! /usr/env/bin python2.6
# -*- coding: utf-8 -*-
"""
    server

    description

    @copyright: 2010 DiogenesAugusto <diofeher@gmail.com>
    @license: see LICENSE.
"""

from socket import socket, AF_INET, SOCK_STREAM
import settings


class Server(object):
    """TCP Socket Server"""
    def __init__(self, host, port):
        """
        Server class used to wrapper sockets
        
        @param s: socket
        @param host: unicode
        @param port: int
        """
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((host, port))
        self.connections = []
        
    def listen(self, max_number):
        """
        @param num: number of maximum connections
        """
        self.socket.listen(max_number)

    def connecting(self):
        con, address = self.socket.accept()
        self.add_connection(con)
        
        while 1:
            data = con.recv(1024)
            if data:
                self.send_broadcast('Hello %s' % data)
            else:
                break
        con.close()

    def add_connection(self, con):
        """
        used to handle all connections
        """
        self.connections.append(con)
        
    def send_msg(self, con, msg):
        """
        send data
        """
        con.send(msg)
        
    def send_broadcast(self, msg):
        for con in self.connections:
            self.send_msg(con, msg)
        
    def receive_msg(self):
        """
        receive data
        """
        pass
    
    def close_connection(self, con):
        """
        close connection
        """
        con.close()


server = Server(settings.HOST, settings.PORT)
server.listen(5)  # maximum of 5 connections

while 1:
    server.connecting()