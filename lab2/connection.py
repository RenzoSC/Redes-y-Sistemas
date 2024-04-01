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
        self.request = b''
        self.connected = True

    def validate_request(self):
        if (self.request.count(b'\n')>1):
            print(error_messages[BAD_EOL] , str(BAD_EOL) + '\r\n')
            self.status = BAD_EOL
            return
        self.request = self.request.decode("utf-8").split()
        if(len(self.request)<2):
            print(error_messages[BAD_EOL], str(BAD_EOL)+'\r\n')
            self.status = BAD_EOL
            return
        if(self.request[0].lower() != "http"):
            print(error_messages[BAD_EOL], str(BAD_EOL) + '\r\n')
            self.status = BAD_EOL
            return
        if(self.request[1] not in VALID_COMMANDS):
            print(error_messages[INVALID_COMMAND], str(INVALID_COMMAND)+ '\r\n')
            self.status = INVALID_COMMAND
            return
        
        if(self.request[1]== 'get_file_listening' and len(self.request)>2):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            return

        if(self.request[1] == 'get_metadata' and len(self.request)!= 3):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            return
        
        if(self.request[1] == 'get_slice' and len(self.request)!= 4):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            return
        self.status = CODE_OK


    def read(self):
        """
        Lee un mensaje completo de la conexión.
        """
        self.request = self.s_connection.recv(1024) # Recibe el mensaje y lo guarda en un buffer para luego parsearlo
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

            if self.status == CODE_OK:
                self.execute(self.request)
