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
                conn.send((pid, msg))  
            else: 
                conn.send(f"mensaje '{msg}' procesado") 
          
# Esta función envia un mensaje al inicio de cada conversación. 
def send_msg(info_receptor, info_emisor):  
    print(f"enviando mensaje a {info_receptor[0]}") 
    with Client(address = (info_receptor[1], info_receptor[2]), authkey = info_receptor[3]) as conn: 
        conn.send((info_emisor, 'informacion del emisor')) 
 
# Esta función devuelve una lista con los nombres de las personas en línea. 
def clients_connected(clients):  
    list_clients_connected = [] 
    for i in clients.items(): 
        list_clients_connected.append(i[1]['nombre']) 
    return list_clients_connected 
 
# Esta función obtiene la informacion de un usuario concreto.
def get_user_info(clients, user): 
    info = []
    for i in clients.items():
        if i[1]['nombre'] == user:
            info = [user, i[1]['address'], i[1]['port'], i[1]['authkey']]
    return info

def serve_client(conn, pid, clients, users):
    connected = True
    while connected:
        try:
            (msg, receptor, emisor) = conn.recv()
            if msg == "lista":
                #mandar la lista de todos los usuarios
                list_clients_connected = clients_connected(clients)
                conn.send(list_clients_connected)
            elif msg == "chat":
                info_receptor = get_user_info(clients, receptor) # conseguir información del receptor
                if info_receptor != []:
                    send_msg(info_receptor, emisor) # mandar un mensaje al receptor
                conn.send(info_receptor) # mandar la información del receptor a quien quiere hablar con él
            elif msg == "informacion del emisor":
                conn.send(receptor)
            else:
                 send_msg_all(pid, msg, clients)
        except EOFError:
            print("conexión interrumpida")
            connected = False
    users.remove(clients[pid]['nombre'])
    del clients[pid]
    send_msg_all(pid, f"información '{pid}' del usuario que ha entrado en el chat ", clients)
    print(pid, 'conexión finalizada')
    send_msg_all(pid, f'Los usuarios conectados son: {users}', clients)
         
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

if __name__ == '__main__':
    ip_address = '192.168.9.6'
    users = []
    
    if len(sys.argv) > 1:
         ip_address = sys.argv[1]
    main(ip_address, users)
