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

    def quit(self):
        """
        Cierra la conexión.
        """
        self.status = CODE_OK
        self.connected = False
        print("Cerrando conexión...")
        self.send_response('')
        self.s_connection.close()

    def get_file_listing(self):
        file_list = os.listdir(path=self.dir)
        body_msg = ""
        for file in file_list:
            body_msg += file + EOL
        self.send_response(body_msg)

    def get_metadata(self, request):
        file = request[2]
        file_list = os.listdir(path=self.dir)
        
        if file not in file_list:
            self.status = FILE_NOT_FOUND
            self.send_response('')
            return
        
        path = f'{self.dir}/{file}'
        metadata = str(os.path.getsize(path))
        self.send_response(metadata)

    def get_slice(self, request):
        file = request[2]
        offset = int(request[3])
        size = int(request[4])
        file_list = os.listdir(path=self.dir)
        if file not in file_list:
            self.status = FILE_NOT_FOUND
            self.send_response('')
            return
        path = f'{self.dir}/{file}'
        tam = os.path.getsize(path)

        if offset > tam:
            self.status = BAD_OFFSET
            self.send_response('')
        
        fd = os.open(path, os.O_RDONLY)

        try:
            os.lseek(fd, offset, os.SEEK_SET)
            bytes_readed = os.read(fd, size)
            bytes_readed = b64encode(bytes_readed)
            self.send_response(bytes_readed)
        except Exception as e:
            print(e)
            self.status = INTERNAL_ERROR
            self.send_response('')
            self.connected = False
            print("Cerrando conexión...")
            self.s_connection.close()
        finally:
            os.close(fd)

    def send_response(self, body):
        status = str(self.status) +' ' + error_messages[self.status] + EOL
        status = status.encode('utf-8')
        self.s_connection.send(status)
        body_msg = body if type(body)== bytes else body.encode('utf-8')
        self.s_connection.send(body_msg)
        self.s_connection.send(EOL.encode('utf-8'))

    def validate_request(self):
        if (not self.request):
            print("No hay ningún cliente conectado...")
            self.status = CODE_OK
            self.connected = False
            print("Cerrando conexión...")
            self.s_connection.close()
            return
        
        if (self.request.count(b'\n')>1):
            print(error_messages[BAD_EOL] , str(BAD_EOL) + '\r\n')
            self.status = BAD_EOL
            return
        self.request = self.request.decode("utf-8").split()
        print(self.request)
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
        
        if(self.request[1] in ['quit', 'get_file_listing'] and len(self.request)>2):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            return
        elif(self.request[1] == 'get_metadata' and len(self.request)!= 3):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            self.s_connection.send(b'invalid arguments')
            return
        elif(self.request[1] == 'get_slice' and len(self.request)!= 5):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            return
        else:
            self.status = CODE_OK


    def read(self):
        """
        Lee un mensaje completo de la conexión.
        """
        self.request = self.s_connection.recv(1024) # Recibe el mensaje y lo guarda en un buffer para luego parsearlo
        return

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
        elif command == 'get_file_listing':
            self.get_file_listing()
        
        

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

            if self.status == CODE_OK and self.connected:
                self.execute(self.request)
