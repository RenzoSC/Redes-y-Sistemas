# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import socket
import os
from constants import *
from base64 import b64encode


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        """
        Inicializa una nueva conexión con un socket ya aceptado.
        """
        self.s_connection = socket
        self.dir = directory
        self.status = CODE_OK
        self.buffer = ''
        self.connected = True
        self.request = None
    

    def validate_request(self, request):
        if (request.count(b'\n')>1):
            print(error_messages[BAD_EOL] , str(BAD_EOL) + b'\r\n')
            return

        if(request[1] not in VALID_COMMANDS):
            print(error_messages[INVALID_COMMAND], INVALID_COMMAND)
            return
        pass

    def read(self):
        """
        Lee un mensaje completo de la conexión.
        """
        self.buffer = self.s_connection.recv(1024).decode('utf-8') # Recibe el mensaje y lo guarda en un buffer para luego parsearlo

        return
    
    def quit(self):
        """
        Cierra la conexión.
        """
        self.s_connection.close()
        self.connected = False

    def execute(self, request):
        """
        Redirecciona el pedido del cliente al método correspondiente.
        """
        # FALTA: Redirigir el pedido al método correspondiente.
        command = request[1]
        if command == 'quit':
            self.quit()
        elif command == 'get_slice':
            self.get_slice(request)
        elif command == 'get_metadata':
            self.get_metadata(request)
        elif command == 'get_file_listening':
            self.get_file_listening(request)
        pass
        

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        if not os.path.exists(self.dir):
            self.status = INTERNAL_ERROR
            self.error()

        while self.connected is True:
            self.read()
            self.validate_request()
            self.execute()
