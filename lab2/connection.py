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

    def close(self):
        try:
            self.s_connection.close()
        except socket.error as e:
            print(f"error cerrando socket: {e}")

    def quit(self):
        """
        Cierra la conexión.
        """
        self.status = CODE_OK
        self.connected = False
        print("Cerrando conexión...")
        self.send_response('')
        self.close()

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
        file = request[1]
        file_list = os.listdir(path=self.dir)
        
        
        
        # Valido el nombre del archivo
        if not self.is_valid_file(file):
            self.status = FILE_NOT_FOUND
            self.send_response('')
            self.status = CODE_OK
            return
        
        if file not in file_list:
            self.status = FILE_NOT_FOUND
            self.send_response('')
            self.status = CODE_OK
            return

        path = f'{self.dir}/{file}'
        metadata = str(os.path.getsize(path))
        self.send_response(metadata)

    def get_slice(self, request):
        file = request[1]
        try:
            offset = int(request[2])
            size = int(request[3])
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
            self.close()
        finally:
            os.close(fd)

    def send_response(self, body):
        if body != '':
            response = (str(self.status) + ' '+ error_messages[self.status]+EOL).encode('utf-8') 
            response += body if type(body)== bytes else body.encode('utf-8')
            response += EOL.encode('utf-8')
        else:
            response = str(self.status) + ' '+ error_messages[self.status]+EOL
            response = response.encode('utf-8')
        try:
            self.s_connection.send(response)
        except BrokenPipeError or ConnectionResetError:
            self.connected = False

    def validate_request(self):
        if (not self.request):
            print("No hay ningún cliente conectado...")
            self.connected = False
            print("Cerrando conexión...")
            self.close()
            self.status = CODE_OK
            return
        
        self.request = self.request.split()
        print(self.request)
        

        if(self.request[0] not in VALID_COMMANDS):
            print(error_messages[INVALID_COMMAND], str(INVALID_COMMAND)+ '\r\n')
            self.status = INVALID_COMMAND
            self.send_response('')
            self.status = CODE_OK
            return
        
        if(self.request[0] in ['quit', 'get_file_listing'] and len(self.request)>1):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            self.send_response('')
            self.status = CODE_OK
            return
        elif(self.request[0] == 'get_metadata' and len(self.request)!= 2):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            self.send_response('')
            self.status = CODE_OK
            return
        elif(self.request[0] == 'get_slice' and len(self.request)!= 4):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            self.send_response('')
            self.status = CODE_OK
            return
        else:
            self.status = CODE_OK





    def read_line(self, buffer):
        """
        Lee un mensaje completo de la conexión.
        """
        while not EOL in buffer and self.connected:
            try:
                buffer += self.s_connection.recv(BUFFER_SIZE).decode("ascii")
            except socket.error:
                print("socketerrorr")
                self.status =BAD_EOL
                self.connected = False
                print("El cliente se desconectó inesperadamente...")
                self.close()
                return "", ""
            except UnicodeError:
                print("unicoderrorr")
                self.status = INTERNAL_ERROR
                self.send_response('')
                self.connected = False
                print("Cerrando conexión...")
                self.close()
        
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
        command = request[0]
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
            self.close()
        buffer = ""
        
        while self.connected:
            
            line, buffer = self.read_line(buffer)
        
            print(f'line: {line} buffer: {buffer}')

            if line == "":
                continue

            elif '\n' in line:
                self.status = BAD_EOL
                self.send_response('')
                self.connected = False
                print("Cerrando conexión...")
                self.close()
            
            else:
                try:
                    # Revisamos el comando guardado en line y lo ejecutamos
                    self.request = line
                    self.validate_request()
                    if self.status == CODE_OK and self.connected:
                        self.execute(self.request)
                except Exception as e:
                    print(f"error exception:    {e}")
                    self.status = INTERNAL_ERROR
                    self.send_response('')
                    self.connected = False
                    print("Cerrando conexión exception ...")
                    self.close()