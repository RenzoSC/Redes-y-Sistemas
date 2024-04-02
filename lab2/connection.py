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

    def is_valid_file(self, filename):
        is_valid = True
        if len(filename) > MAX_FILENAME or not isinstance(filename, str) or len(filename) == 0:
            is_valid = False
        elif not all(c.isalnum() or c in '-._' for c in filename):
            is_valid = False
        return is_valid
    
    def get_metadata(self, request):
        file = request[2]
        file_list = os.listdir(path=self.dir)
        
        if file not in file_list:
            self.status = FILE_NOT_FOUND
            self.send_response('')
            return
        
        # Valido el nombre del archivo
        elif not self.is_valid_file(file):
            self.status = INVALID_ARGUMENTS
            self.send_response('')
            return

        path = f'{self.dir}/{file}'
        metadata = str(os.path.getsize(path))
        self.send_response(metadata)

    def get_slice(self, request):
        file = request[2]
        try:
            offset = int(request[3])
            size = int(request[4])
        except ValueError:
            self.status = INVALID_ARGUMENTS
            self.send_response('')
            self.status = CODE_OK
            return
        
        file_list = os.listdir(path=self.dir)
        if file not in file_list:
            self.status = FILE_NOT_FOUND
            self.send_response('')
            self.status = CODE_OK
            return
        path = f'{self.dir}/{file}'
        tam = os.path.getsize(path)

        if offset > tam:
            self.status = BAD_OFFSET
            self.send_response('')
            self.status = CODE_OK
            return
        
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
        if body != '':
            response = (str(self.status) + ' '+ error_messages[self.status]+EOL).encode('utf-8') 
            response += body if type(body)== bytes else body.encode('utf-8')
            response += EOL.encode('utf-8')
            i = self.s_connection.send(response)
            print(i)
        else:
            response = str(self.status) + ' '+ error_messages[self.status]+EOL
            response = response.encode('utf-8')
            i = self.s_connection.send(response)
            print(i)

    def validate_request(self):
        if (not self.request):
            print("No hay ningún cliente conectado...")
            self.connected = False
            print("Cerrando conexión...")
            self.s_connection.close()
            self.status = CODE_OK
            return
        
        if (self.request.count(b'\n')>1):
            print(error_messages[BAD_EOL] , str(BAD_EOL) + '\r\n')
            self.status = BAD_EOL
            self.send_response('')
            self.connected = False
            self.s_connection.close()
            return
        self.request = self.request.decode("utf-8").split()
        print(self.request)
        if(len(self.request)<2):
            print(error_messages[BAD_EOL], str(BAD_EOL)+'\r\n')
            self.status = BAD_EOL
            self.send_response('')
            self.connected = False
            self.s_connection.close()
            return
        if(self.request[0].lower() != "http"):
            print(error_messages[BAD_EOL], str(BAD_EOL) + '\r\n')
            self.status = BAD_EOL
            self.send_response('')
            self.connected = False
            self.s_connection.close()
            return
        if(self.request[1] not in VALID_COMMANDS):
            print(error_messages[INVALID_COMMAND], str(INVALID_COMMAND)+ '\r\n')
            self.status = INVALID_COMMAND
            self.send_response('')
            return
        
        if(self.request[1] in ['quit', 'get_file_listing'] and len(self.request)>2):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            self.send_response('')
            return
        elif(self.request[1] == 'get_metadata' and len(self.request)!= 3):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            self.send_response('')
            return
        elif(self.request[1]== 'get_metadata' and len(self.request)==3 and len(self.request[2])>=100):
            self.status = BAD_REQUEST
            self.send_response('')
            self.connected = False
            self.s_connection.close()
            return
        elif(self.request[1] == 'get_slice' and len(self.request)!= 5):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            self.send_response('')
            return
        else:
            self.status = CODE_OK


    def read_line(self, buffer):
        """
        Lee un mensaje completo de la conexión.
        """
        while not EOL in buffer and self.connected:
            try:
                buffer += self.socket.recv(BUFFER_SIZE).decode("ascii")
            except UnicodeError:
                self.send_response('')
                self.connected = False
                print("Cerrando conexión...")
        
        if EOL in buffer:
            line, buffer = buffer.split(EOL,1)
            line = line.strip()
            return line, buffer
        else:
            return "",""

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
            self.connected = False
            self.s_connection.close()
        buffer = ""
        while self.connected:
            line, buffer = self.read_line(buffer)
            
            if line == "":
                continue

            elif '\n' in line:
                self.send_response('')
                self.connected = False
                print("Cerrando conexión...")
            
            else:
                try:
                    #Parseamos el comando y lo ejecutamos


