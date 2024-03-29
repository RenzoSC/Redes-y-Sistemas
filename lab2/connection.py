# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import socket
from constants import *
from base64 import b64encode

class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        self.s_connection = socket
        self.dir = directory
        pass
    
    def validate_request(self, request):
        if (request.count(b'\n')>1):
            print(error_messages[BAD_EOL] , str(BAD_EOL) + b'\r\n')
            return
        request = request.decode("utf-8").split()

        if(request[1] not in VALID_COMMANDS):
            print(error_messages[INVALID_COMMAND], INVALID_COMMAND)
            return
        pass

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        while True:
            request = self.s_connection.recv(1024)
            print(request.count(b'\n'))
            self.validate_request(request=request)
            request = request.decode("utf-8")
            request = request.strip()
            if(request=='quit'):
                print("cerrando conexión con cliente...")
                self.s_connection.close()
                break