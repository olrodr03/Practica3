"""
PROGRAMACIÓN DISTRIBUIDA
------------------------
Práctica 3: Chat

Autoras: Claudia Casado Poyatos
         Natalia García Domínguez
         Olga Rodríguez Acevedo
"""
from multiprocessing.connection import Client, Listener
from time import sleep
from multiprocessing import Process
import sys, os
import traceback

def client_listener(info, conexion, fn):
    print(f"**************Abriendo 'listener' desde {info}**************")
    cl = Listener(address = (info['address'], info['port']), authkey = info['authkey'])
    print("**************Iniciando 'listener'**************")
    while True:
        conn = cl.accept()
        print("**************Aceptando conexiones desde", cl.last_accepted)
        m = conn.recv()
        print("**************mensaje recibido:", m)
        if m[1] == 'información del emisor': 
            #debemos cerrar la conexión entre el cliente que recibe este mensaje y el servidor
            print('Este usuario quiere entablar una conversación')
            conexion.send(("información del emisor", m[0], 0))
            print('Escribe "ACEPTO" si quieres iniciarla. Saluda para avisar de que estás en el chat')

# Función para la persona que quiere iniciar la conversación.
def emisor_connection(client_info, fn): 
    print("**************Intentando conectar**************")
    sys.stdin = os.fdopen(fn)
    with Client(address=(client_info['address'], client_info['port']), authkey=client_info['authkey']) as conn: #Información del emisor
        
        sleep(1)
        print("**************Aceptando conexiones**************")
        connected = True
        while connected:
        
            message_sent = input('¿Qué quieres hacer?\n Si quieres hablar, escribe tu mensaje.\n Si quieres mandar un fichero, escribe "archivo".\n Si quieres desconectarte del chat, escribe "salir"\n')
            
            if message_sent == 'archivo':
                conn.send(message_sent)
                archive = input('Dime el nombre del archivo: ')
                f = open(archive, 'r')
                f_lines = f.readlines()
                f.close()
                conn.send(archive)
                conn.send(f_lines)
            elif message_sent == 'salir':
                conn.send('El usuario se ha desconectado')
                connected = False
            else:
                conn.send(message_sent)
            message_received = conn.recv()
            print(message_received)
            if message_received == 'El usuario se ha desconectado':
                connected = False
            elif message_received == 'archivo':
                name_archive = conn.recv()
                f_lines = conn.recv()
                f = open(name_archive, 'w')
                f.writelines(f_lines)
                f.close()
                print("Te han enviado este archivo: ", name_archive)
        print("**************Conexión cerrada**************")
        conn.close()
    print("**************Cerrando la conexión entre los clientes**************")

# Función para la persona que acepta iniciar la conversación.
def receptor_connection(conn, fn):
    sys.stdin = os.fdopen(fn)
    connected = True
    while connected:
        try:
            message_received = conn.recv()
            print(message_received)
            if message_received == 'El usuario se ha desconectado':
                connected = False
            elif message_received == 'archivo':
                name_archive = conn.recv()
                f_lines = conn.recv()
                f = open(name_archive, 'w')
                f.writelines(f_lines)
                f.close()
                print("Te han enviado este archivo: ", name_archive)
            message_sent = input('¿Qué quieres hacer?\n Si quieres hablar, escribe tu mensaje.\n Si quieres mandar un fichero, escribe "archivo".\n Si quieres desconectarte del chat, escribe "salir"\n')
            if message_sent == 'archivo':
                conn.send(message_sent)
                archive = input('Dime el nombre del archivo: ')
                f = open(archive, 'r')
                f_lines = f.readlines()
                f.close()
                conn.send(archive)
                conn.send(f_lines)
            elif message_sent == 'salir':
                conn.send('El usuario se ha desconectado')
                connected = False
            else:
                conn.send(message_sent)
        except EOFError:
            print("**************Conexión imterrumpida**************")
            connected = False
    print("**************Conexión cerrada**************")
    conn.close()
    print("**************Cerrando la conexión entre los clientes**************") # Finalizada la conversación vuelven al servidor

def connection(info_emisor, info_receptor, fn):
    print("**************Abriendo conexión entre los clientes**************")
    with Listener(address = (info_emisor['address'], info_emisor['port']), authkey = info_emisor['authkey']) as listener:
        print("**************Iniciando 'listener'**************")
        while True:
            print("**************Aceptando conexiones**************")
            try:
                conn = listener.accept()
                print(info_receptor[0], "ha aceptado hablar contigo")
                p = Process(target = receptor_connection, args = (conn, fn, ))
                p.start()
            except Exception as e:
                traceback.print_exc()
        print("**************Servidor cerrado**************")
         
def main(server_address, info):
    print("**************Intentando conectar**************")
    with Client(address = (server_address, 6000), authkey = b'secret password server') as conn:
        fn = sys.stdin.fileno()
        cl = Process(target = client_listener, args = (info, conn, fn, ))
        cl.start()
        sleep(1)
        conn.send(info)
        connected = True
        while connected:
            command = input('Escribe "lista" si quieres conocer los usuarios en línea o \n "chat" si quieres iniciar una conversación \n')
            if command == "lista":
                conn.send((command, 0, 0))
                list_clients_connected = conn.recv()
                print("Los usuarios conectados son:", list_clients_connected)
            elif command == "chat":
                user = input('¿Con quién quieres hablar? ')
                conn.send((command, user, info))
                info_user == conn.recv()
                if info_user == []:
                    print("Nombre incorrecto. Vuelve a intentarlo.")
                else:
                    connected = False
                    conn.close()
                    cl.terminate()
                    connection1 = Process(target = connection, args = (info, info_user, fn, ))
                    conection1.start()
            elif command == "salir":
                connected = False
                conn.close()
            elif command == "ACEPTO":
                info_client = conn.recv()
                connected = False
                conn.close()
                cl.terminate()
                connection_emisor = Process(target = emisor_connection, args = (info_client, fn, ))
                connection_emisor.start()
        cl.terminate()

if __name__ == '__main__':
    server_address = '192.168.9.6' # Dirección IP del 'broker'.
    client_address = '' # Dirección IP del 'client'.
    client_port = 6001
              
    nombre = input('¿Cuál es tu nombre? ')
    if len(sys.argv) > 1:
        client_port = int(sys.argv[1])
    if len(sys.argv) > 2:
        client_address= sys.argv[2]
    if len(sys.argv) > 3:
        server_address= sys.argv[3]
    info = {'nombre': nombre, 'address': client_address, 'port': client_port, 'authkey': b'secret client server'}
    main(server_address, info)             
