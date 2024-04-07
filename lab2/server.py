#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import optparse
import socket
import sys
import threading
import os
import connection
from constants import *


class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT,
                 directory=DEFAULT_DIR):
        print("Serving %s on %s:%s." % (directory, addr, port))

        if not os.path.isdir(directory):
            os.mkdir(directory)

        self.server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind((addr,port))
        self.dir = directory
        self.server_socket.listen(MAX_CONNECTIONS)
        self.threadLimiter = threading.BoundedSemaphore(MAX_CONNECTIONS)

        print("Server ready. Waiting connections...")

    def handle(self, connection):
        """
        Atiende una conexión. Recibe un objeto Connection y se encarga
        de manejarla.
        """
        self.threadLimiter.acquire()
        def handler():
            try:
                connection.handle()
            finally:
                self.threadLimiter.release()
        t = threading.Thread(target=handler)
        t.start()
        """
        El patrón que te mostré anteriormente, donde el bloque finally dentro del método handle() de Connection se encarga de 
        cerrar la conexión y limpiar recursos, es suficiente para garantizar que el hilo de ejecución termine adecuadamente, 
        liberando el bloqueo adquirido previamente con acquire().
        Por lo tanto, si confías en que Connection.handle() manejará adecuadamente la terminación del hilo y la liberación de
        recursos, no necesitarías llamar explícitamente a release() después de acquire() en el método serve() del servidor.
        """

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez
        y se espera a que concluya antes de seguir.
        """
        while True:
            # FALTA: Aceptar una conexión al server, crear una
            # Connection para la conexión y atenderla hasta que termine.
            client,addr = self.server_socket.accept()
            connection_c = connection.Connection(client,self.dir)
            self.handle(connection_c)
            
def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    server = Server(options.address, port, options.datadir)
    server.serve()


if __name__ == '__main__':
    main()
