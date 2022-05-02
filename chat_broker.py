"""
PROGRAMACIÓN DISTRIBUIDA
------------------------
Práctica 3: Chat

Autoras: Claudia Casado Poyatos
         Natalia García Domínguez
         Olga Rodríguez Acevedo
"""

from multiprocessing.connection import Listener, Client
import sys
from multiprocessing import Process, Manager
import traceback

def send_msg_all(pid, msg, clients):
    for client, client_info in clients.items():
        print(f"enviando: '{msg}' a {client_info}")
        with Client(address = (client_info['address'], client_info['port']), authkey = client_info['authkey']) as conn:
            if not client == pid:
                conn.send((pid,msg))
            else:
                conn.send(f"mensaje '{msg}' procesado")

def send_msg(info_receptor,info_emisor): #Para enviar un mensaje al inicio de cada conversación
  print(f"enviando mensaje a {info_receptor[0]}")
  with Client(addres=(info_receptor[1],info_receptor[2]), authkey=info_receptor[3]) as conn:
    conn.send((info_emisor, 'informacion del emisor'))

def clients_connected(clients): #Esta funcion devuelve una lista con los nombres de las personas en linea
  list_clients_connected=[]
  for i in clients.items():
    list_clients_connected.append(i[1]['nombre'])
    return list_clients_connected

def get_user_info(clients,user): #funcion que obtiene la informacion del usuario
  info = []
  for i in clients.items():
    if i[1]['nombre']==user:
      info= [user, i[1]['address'], i[1]['port'], i[1]['authkey']]
  return info

def main(ip_address, users):
    with Listener(address = (ip_address, 6000), authkey = b'secret password server') as listener:
        print('comenzando "listener"')

        m = Manager()
        clients = m.dict()

        while True:
            print('aceptando conexiones')
            try:
                conn = listener.accept()
                print('IP del usuario conectado', listener.last_accepted)
                client_info = conn.recv()
                users.append(client_info['nombre'])
                pid = listener.last_accepted
                clients[pid] = client_info
                  
                send_msg_all(pid, f"IP del nuevo usuario: {pid}", clients)
                send_msg_all(pid, f"Los clientes conectados son: {users}", clients)
                p = Process(target = serve_client, args = (conn, listener.last_accepted, clients, users))
                p.start()
                 
                except Exception as e:
                    traceback.print_exc()
                print('Chat cerrado')
