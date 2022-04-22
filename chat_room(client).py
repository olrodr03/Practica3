"""
ENTREGA 3
Chat Room - Client

Olga Rodríguez Acevedo
Claudia Casado Poyatos
Natalia García Domínguez
"""

from multiprocessing.connection import Client, Listener
from time import sleep
from multiprocessing import Process
import sys, os
import traceback

def client_listener(info, conexion, fn):
    print("Openning listener at {info}")
    cl = Listener(address=(info['address'], info['port']), authkey=info['authkey'])
    print(".......................client listener comenzando")
    print(".......................aceptando conexiones")
    while True:
        conn = cl.accept()
        print(".......................conexión aceptada por", cl.last_accepted)
        m = conn.recv()
        print(".......................mensaje recibido", m)
        if m[1] == 'Alguien quiere hablar contigo':
            print(m[1])
            conexion.send(("info del usuario que quiere hablar conmigo", m[0], 0))
            print('Escribe por pantalla: ACEPTO')
            
def nueva_conexion(info_client, fn):
    print("Intentando conectar")
    sys.stadin = os.fdopen(fn)
    with Client(address=(info_client['address'], info_client['port']), authkey=info_client['authkey']) as conn:
        
        sleep(1)
        print(".......................aceptando conexiones")
        conectado = True
        while conectado:
            
            msg_a_enviar = input('¿Qué mensaje quieres mandar?\nescribe "quit" para desconectarte o\n"fichero" para mandar un fichero\n')
            if msg_a_enviar == 'quit':
                conn.send('El usuario se ha desconectado')
                conectado = False
            elif msg_a_enviar == 'fichero':
                conn.send(msg_a_enviar)
                
                fichero = input('Dime el nombre del fichero:')
                f = open(fichero, 'r')
                f_lines = f.readlines()
                f.close()
                conn.send(fichero)
                conn.send(f_lines)
            else:
                conn.send(msg_a_enviar)
            msg_a_recibir = conn.recv()
            print(msg_a_recibir)
            if msg_a_recibir == 'El usuario se ha desconectado':
                conectado = False
            elif msg_a_recibir == 'fichero':
                nombre_fichero = conn.recv()
                f_lines = conn.recv()
                f = open(nombre_fichero, 'w')
                f.writelines(f_lines)
                f.close()
                print("Has recibido el fichero:", nombre_fichero)
        print("Conexión cerrada")
        conn.close()
    print(".......................Conexión terminada entre los dos clients")

def client_client2(conn, fn): # Esta es para la persona con quien quieren hablar
    sys.stdin = os.fdopen(fn)
    connected = True
    while connected:
        try:
            msg_a_recibir = conn.recv()
            print(msg_a_recibir)
            if msg_a_recibir == 'El usuario se ha desconectado':
                connected = False
            elif msg_a_recibir == 'fichero':
                nombre_fichero = conn.recv()
                f_lines = conn.recv()
                f = open(nombre_fichero, 'w')
                f.writelines(f_lines)
                f.close()
                print("Has recibido el fichero:", nombre_fichero)
              
            msg_a_enviar = input('Qué mensaje quieres mandar?\nEscribe "quit" para desconectarte o\n"fichero" para mandar un fichero\n')
          
            if msg_a_enviar == 'quit':
                conn.send('El usuario se ha desconectado')
                connected = False
            elif msg_a_enviar == 'fichero':
                conn.send(msg_a_enviar)
                fichero = input('Dime el nombre del fichero:')
                f = open(fichero, 'r')
                f_lines = f.readlines()
                f.close()
                conn.send(fichero)
                conn.send(f_lines)
            else:
                conn.send(msg_a_enviar)
        except EOFError:
            print("connection abruptly closed by client")
            connected = False
    print("Connection closed")
    conn.close()
    print(".......................Ending connection between two clients")
# Esto sería una vez que se ha acabado la conexión entre los dos que están hablando para volver al servidor

def client_client(info, user_info, fn): # El que pide hablar con alguien hace de broker falso
    print(".......................Openning connection between two clients")
    # info es la información de uno mismo (diccionario)
    # user_info son los datos de la persona con la que quieres hablar (lista)
    
    with Listener(address = (info['address'], info['port']), authkey = info['authkey']) as listener:
        print("listener starting")
        
        while True:
            print("accepting connexions")
            try:
                conn = listener.accept()
                print("connection accepted from", user_info[0])
                
                p = Process(target = client_client2, args = (conn, fn, ))
                p.start()
            except Exception as e:
                traceback.print_exc()
                
        print("end server")
