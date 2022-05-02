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
    cl = Listener(address = (info['address'], info['port']), authkey = info['authkey'])
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
    with Client(address = (info_client['address'], info_client['port']), authkey = info_client['authkey']) as conn:
        
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
    print(".......................Terminando conexión entre los dos clients")

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
            print("conexión cerrada de manera abrupta por client")
            connected = False
    print("Conexión cerrada")
    conn.close()
    print(".......................Terminando conexión entre los dos clients")
# Esto sería una vez que se ha acabado la conexión entre los dos que están hablando para volver al servidor

def client_client(info, user_info, fn): # El que pide hablar con alguien hace de broker falso
    print(".......................Iniciando conexión entre dos clients")
    # info es la información de uno mismo (diccionario)
    # user_info son los datos de la persona con la que quieres hablar (lista)
    
    with Listener(address = (info['address'], info['port']), authkey = info['authkey']) as listener:
        print("listener comenzando")
        
        while True:
            print("aceptando conexiones")
            try:
                conn = listener.accept()
                print("conexión aceptada por", user_info[0])
                
                p = Process(target = client_client2, args = (conn, fn, ))
                p.start()
            except Exception as e:
                traceback.print_exc()
                
        print("end server")
def main(server_address, info):
    print("Intentando conectarse.............")
    with Client(address=(server_address, 6000), authkey=b'secret password server') as conn:
        fn= sys.stdin.fileno()
        cl = Process(target=client_listener, args=(info,conn,fn,))
        cl.start()
        sleep(1)
        conn.send(info)
        coneccted=True
        while coneccted:
            command = input('Introduce "getlist" si quieres saber las personas conectadas o \n"connect" si quieres iniciar una conversación \n')
            if command =="getlist":
                conn.send((command,0,0))
                userlist = conn.recv()
                print("En linea...")
                print("Los usuarios conectados son:", userlist)
            elif command == "connect":
                usuario = input('¿Con quién quieres hablar? ')
                conn.send((commad, usuario, info))
                user_info = conn.recv()
                if user_info == []:
                    print("No se corresponde con ninguún usuario conectado. Pruebe de nuevo. ")
                else:
                    connected= False
                    conn.close()
                    cl.terminate()
                    connection1 = Process(target= client_client, args = (info, user_info, fn,))
                    conecction1.start()
           elif command =="quit":
                connected = False
                conn.close()
           elif command =="ACEPTO":
                info_client = conn.recv()
                connected = False
                conn.close()
                cl.terminate()
                conecction2 = Process(target=nueva_conexion, args =(info_client, fn,,))
                conecction2.start()
          cl.terminate()
    print("cliente cerrado")

 if __name__ == '__main__':
    server_address = '192.168.4.5'
    client_address =  '192.168.4.6'
    client_port =6001
    
    nombre = input('¿Cómo te llamas? ')
    
    if len(sys.argv) >1:
        client_port = int(sys.argv[1])
    if len(sys.argv) >2:
        client_address = sys.argv[2]
    if len(sys.argv) >3:
        server.address = sys.argv[3]
    info 0 {'nombre': nombre, 'address': client_address, 'port': client_port, 'authkey': b'secret client server'}
    main(server_address,info)

            
            
    
