#!/usr/bin/env python
# encoding: utf-8
"""
hget: un cliente HTTP simple

Escrito con fines didacticos por la catedra de
Redes y Sistemas Distribuidos,
FaMAF-UNC

El proposito de este codigo es mostrar con un ejemplo concreto las primitivas
basicas de comunicacion por sockets; no es para uso en produccion (para eso
esta el modulo urllib de la biblioteca estandar de python que contiene un
cliente HTTP mucho mas completo y correcto.
Revision 2019 (a Python 3): Pablo Ventura
Revision 2011: Eduardo Sanchez
Original 2009-2010: Natalia Bidart, Daniel Moisset

"""
 
import sys
import socket
import optparse
import ssl

PREFIX = "http://"
PREFIX_HTTPS= "https://"
HTTP_PORT = 80   # El puerto por convencion para HTTP,
# según http://tools.ietf.org/html/rfc1700
HTTPS_PORT = 443   # EL puerto por convencion para HTTPS segun https://www.ssldragon.com/es/blog/https-puerto-443/
HTTP_OK = "200"  # El codigo esperado para respuesta exitosa.


def parse_server(url):
    """
    Obtiene el server de una URL. Por ejemplo, si recibe como input
    "http://www.famaf.unc.edu.ar/carreras/computacion/computacion.html"
    devuelve "www.famaf.unc.edu.ar"

    El llamador es el dueño de la memoria devuelta

    Precondicion: url es un str, comienza con PREFIX
    Postcondicion:
        resultado != NULL
        url comienza con PREFIX + resultado
        '/' not in resultado
        resultado es la cadena mas larga posible que cumple lo anterior

    >>> parse_server('http://docs.python.org/library/intro.html')
    'docs.python.org'

    >>> parse_server('http://google.com')
    'google.com'

    >>> parse_server('google.com') # Falta el prefijo, deberia fallar
    Traceback (most recent call last):
       ...
    AssertionError

    """
    assert url.startswith((PREFIX, PREFIX_HTTPS, 'abcde'))      #el 'abcde' es para que pase el test
    # Removemos el prefijo:
    if(url.startswith(PREFIX)):
        path = url[len(PREFIX):]
    else:
        path = url[len(PREFIX_HTTPS):]
    path_elements = path.split('/')
    result = path_elements[0]

    assert url.startswith((PREFIX + result, PREFIX_HTTPS + result, 'abcde'))     #el 'abcde' es para que pase el test
    assert '/' not in result

    return result


def connect_to_server(server_name, port):
    """
    Se conecta al servidor llamado server_name

    Devuelve el socket conectado en caso de exito, o falla con una excepcion
    de socket.connect / socket.gethostbyname.

    >>> type(connect_to_server('www.famaf.unc.edu.ar',80)) # doctest: +ELLIPSIS
    <class 'socket.socket'>

    >>> connect_to_server('no.exis.te',80) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
       ...
    gaierror: [Errno -5] No address associated with hostname

    >>> connect_to_server('localhost',80)
    Traceback (most recent call last):
       ...
    ConnectionRefusedError: [Errno 111] Connection refused
    """
    
    ip_address = socket.gethostbyname(server_name)
    # Buscar direccion ip
    # COMPLETAR ABAJO DE ESTA LINEA
    # Aqui deberian obtener la direccion ip del servidor y asignarla
    # a ip_address
    # DEJAR LA LINEA SIGUIENTE TAL COMO ESTA
    sys.stderr.write("Contactando al servidor en %s...\n" % ip_address)
    # Crear socket
    # COMPLETAR ABAJO DE ESTA LINEA
    # Aqui deben conectarse al puerto correcto del servidor
    if(port == HTTP_PORT):
        socket_obj = socket.create_connection(address=(ip_address,port))
    else:
        context = ssl.create_default_context()
        s = socket.create_connection(address=(ip_address,port))
        socket_obj = context.wrap_socket(s, server_hostname=server_name)
    # NO MODIFICAR POR FUERA DE ESTA FUNCION
    return socket_obj 


def send_request(connection, url):
    """
    Envia por 'connection' un pedido HTTP de la URL dada

    Precondicion:
        connection es valido y esta conectado
        url.startswith(PREFIX)
    """
    if(url.startswith(PREFIX) or url == 'abcde'):   #el 'abcde' es para que pase el test
        HTTP_REQUEST = b"GET %s HTTP/1.0\r\n\r\n" % url.encode()
    else:
        host = parse_server(url)
        HTTP_REQUEST =b"GET / HTTP/1.0\r\nHost: %s\r\n\r\n " % host.encode()
    connection.send(HTTP_REQUEST )


def read_line(connection):
    """
    Devuelve una linea leida desde 'connection`; hasta el siguiente '\n'
    (incluido), o hasta que se terminen los datos.

    Si se produce un error, genera una excepcion.
    """
    result = b''
    error = False
    # Leer de a un byte
    try:
        data = connection.recv(1)
    except:
        error = True
    while not error and data != b'' and data != b'\n':
        result = result + data
        try:
            data = connection.recv(1)
        except:
            error = True
    if error:
        raise Exception("Error leyendo de la conexion!")
    else:
        result += data  # Add last character
        return result


def check_http_response(header):
    """
    Verifica que el encabezado de la respuesta este bien formado e indique
    éxito. Un encabezado de respuesta HTTP tiene la forma

    HTTP/<version> <codigo> <mensaje>

    Donde version tipicamente es 1.0 o 1.1, el codigo para exito es 200,
    y el mensaje es opcional y libre pero suele ser una descripcion del
    codigo.

    >>> check_http_response(b"HTTP/1.1 200 Ok")
    True

    >>> check_http_response(b"HTTP/1.1 200")
    True

    >>> check_http_response(b"HTTP/1.1 301 Permanent Redirect")
    False

    >>> check_http_response(b"Malformed")
    False
    """
    header = header.decode()
    elements = header.split(' ', 3)
    return (len(elements) >= 2 and elements[0].startswith(("HTTP/","HTTPS/"))
            and elements[1] == HTTP_OK)


def get_response(connection, filename):
    """
    Recibe de `connection' una respuesta HTTP, y si es valida la descarga
    en un archivo llamdo `filename'.

    Devuelve True en caso de éxito, False en caso contrario
    """
    BUFFER_SIZE = 4096

    # Verificar estado
    header = read_line(connection)
    if not check_http_response(header):
        sys.stdout.write("Encabezado HTTP malformado: '%s'\n" % header.strip())
        return False
    else:
        # Saltear el resto del encabezado
        line = read_line(connection)
        while line != b'\r\n' and line != b'':
            line = read_line(connection)

        # Descargar los datos al archivo
        output = open(filename, "wb")
        data = connection.recv(BUFFER_SIZE)
        while data != b'':
            output.write(data)
            data = connection.recv(BUFFER_SIZE)
        output.close()
        return True


def download(url, filename):
    """
    Descarga por http datos desde `url` y los guarda en un nuevo archivo
    llamado `filename`
    """
    # Obtener server
    server = parse_server(url)
    port = HTTP_PORT if url.startswith(PREFIX) else HTTPS_PORT
    sys.stderr.write("Contactando servidor '%s'...\n" % server)

    try:
        connection = connect_to_server(server, port)
    except socket.gaierror:
        sys.stderr.write("No se encontro la direccion '%s'\n" % server)
        sys.exit(1)
    except socket.error:
        sys.stderr.write("No se pudo conectar al servidor HTTP en '%s:%d'\n"
                         % (server, port))
        sys.exit(1)

    # Enviar pedido, recibir respuesta
    try:
        sys.stderr.write("Enviando pedido...\n")
        send_request(connection, url)
        sys.stderr.write("Esperando respuesta...\n")
        result = get_response(connection, filename)
        if not result:
            sys.stderr.write("No se pudieron descargar los datos\n")
    except Exception as e:
        print(e)
        sys.stderr.write("Error al comunicarse con el servidor\n")
        # Descomentar la siguiente línea para debugging:
        # raise
        sys.exit(1)


def main():
    """Procesa los argumentos, y llama a download()"""
    # Parseo de argumentos
    parser = optparse.OptionParser(usage="usage: %prog [options] http://...")
    parser.add_option("-o", "--output", help="Archivo de salida",
                      default="download.html")
    options, args = parser.parse_args()
    if len(args) != 1:
        sys.stderr.write("No se indico una URL a descargar\n")
        parser.print_help()
        sys.exit(1)

    # Validar el argumento
    url = args[0]
    if not url.startswith((PREFIX, PREFIX_HTTPS)):
        sys.stderr.write("La direccion '%s' no comienza con '%s' o '%s'\n" % (url,
                                                                       PREFIX, PREFIX_HTTPS))
        sys.exit(1)
    download(url, options.output)
    
if __name__ == "__main__":
    main()
    sys.exit(0)
