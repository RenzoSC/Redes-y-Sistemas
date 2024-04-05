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
            response = (str(self.status) + ' '+ error_messages[self.status]+EOL).encode('ascii') 
            response += body if type(body)== bytes else body.encode('ascii')
            response += EOL.encode('ascii')
        else:
            response = str(self.status) + ' '+ error_messages[self.status]+EOL
            response = response.encode('ascii')
        try:
            self.s_connection.send(response)
        except Exception as e:
            print(f"exception sending response: {e}")
            self.connected = False

    def validate_request(self):
        # if (not self.request):
        #     print("No hay ningún cliente conectado...")
        #     self.connected = False
        #     print("Cerrando conexión...")
        #     self.close()
        #     self.status = CODE_OK
        #     return
        
        self.request = self.request.split()
        print(self.request)
        

        if(self.request[0] not in VALID_COMMANDS):
            print(error_messages[INVALID_COMMAND], str(INVALID_COMMAND)+ '\r\n')
            self.status = INVALID_COMMAND
            self.send_response('')
            return
        
        if(self.request[0] in ['quit', 'get_file_listing'] and len(self.request)>1):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            self.send_response('')
            return
        elif(self.request[0] == 'get_metadata' and len(self.request)!= 2):
            print(error_messages[INVALID_ARGUMENTS], str(INVALID_ARGUMENTS) + '\r\n')
            self.status = INVALID_ARGUMENTS
            self.send_response('')
            return
        elif(self.request[0] == 'get_slice' and len(self.request)!= 4):
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
                buffer += self.s_connection.recv(BUFFER_SIZE).decode("ascii")
            except socket.error:
                print("socketerrorr")
                self.status =BAD_EOL
                self.connected = False
                print("El cliente se desconectó inesperadamente...")
                self.close()
                return ""
            except UnicodeError :
                print("unicoderrorr")
                self.status = INTERNAL_ERROR
                self.send_response('')
                self.connected = False
                print("Cerrando conexión...")
                self.close()
                return ""
        
        if EOL in buffer:
            buffer = buffer.strip()
            return buffer
        else:
            return ""




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
        buffer = []
        line = ""
        full = False

        while self.connected:
            
            line = self.read_line(line)
            
            while (line != ""):
                if '\n' in line:
                    self.status = BAD_EOL
                    self.send_response('')
                    self.connected = False
                    print("Cerrando conexión...")
                    self.close()
                else:
                    buffer.append(line)
                    print(f'line: {line} endline')
                    print(f'buffer: {buffer} endbuffer')
                    full = True
                    line = ""

                    #Aca quiero hacer que lea a ver si hay otra linea
                    #el problema es que read_line espera infinitamente hasta encontrarla
                    #asi que nuenca vuelve cuando se acaban, habria que ver cuando se acaba y ahi
                    #dejar de leer. si se hace eso el buffer funcionaria y nomas faltaria hacer que 
                    #solo imprimera el 0ok para el primero en el for de abajo
                    #taria bueno algo tipo line = next(file) y si no hay que levante un flag que se pueda
                    #checkear o algo, pero no se como hacerlo aca
                    line = self.read_line(line)

            if not full:
                continue

            else:
                for command in buffer:
                    line = command
                    buffer.pop()
                    try:
                        # Revisamos el comando guardado en line y lo ejecutamos
                        self.request = line
                        self.validate_request()
                        if self.status == CODE_OK and self.connected:
                            self.execute(self.request)
                            self.status = CODE_OK
                    except Exception as e:
                        print(f"error exception:    {e}")
                        self.status = INTERNAL_ERROR
                        self.send_response('')
                        self.connected = False
                        print("Cerrando conexión exception ...")
                        self.close()
                line = ""
                full = False
        self.close()