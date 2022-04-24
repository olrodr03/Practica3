"""
ENTREGA 3 
Chat Room - Broker

Olga Rodríguez Acevedo
Claudia Casado Poyatos
Natalia García Domínguez

"""
from multiprocessing.connection import Listener, Client
import sys
from multiprocessing import Process, Manager
import traceback

def send_msg_all(pid, msg, clients):
    for client, client_info in clients.items():
        print(f"enviando {msg} a {client_info}")
        with Client(address = (client_info['address'],client_info['port']),authkey=client_info['authkey']) as conn:
            if not client == pid:
                conn.send((pid,msg))
            else:
                conn.send(f"mensaje {msg} procesado")
def send_msg(info_s,info_p):
    print(f"enviando un mensaje a {info_s[0]}")
    with Client(address=(info_s[1],info_s[2]), authkey = info_s[3]) as conn:
        conn.send((info_p,'Quieren empezar una conversación'))
def get_all_clients_connected(clients): 
    all_clients_coneccted = []
    for j in clients.items():
        all_clients_connected.append(j[1]['nombre'])
    return all_clients_connected

def get_info(clients,usuario):
    s = []
    for i in clients.items():
        if i[1]['nombre'] == usuario:
            s = [usuario, i[1]['address'], i[1]['port'], i[1]['authkey']]
    return s

def serve_client(conn, pid, clients, usuarios):
    connected = True
    while connected:
        try:
            (m, s, p) = conn.recv()
            if m == 'getlist':
                all_clients_connected = get_all_clients_connected(clients)
                conn.send(all_clients_connected)
            elif m == 'connect':
                info_s = get_info(clients, s)
                if info_s != []:
                    send_msg(info_s,p)
                conn.send(info_s)
            elif m == 'info del usuario que quiere hablar conmigo':
                conn.send(s)
            else:
                send_msg_all(pid, m, clients)
        except EOFError:
            print('conexión interrumpida por el client')
            connected = False
    usuarios.remove(clients[pid]['nombre'])
    del clients[pid]
    send_msg_all(pid, f'Los usuarios conectados son: {usuarios}', clients)

def main(ip_address, usuarios):
    with Listener(address = (ip_address, 6000), authkey = b'secret password server') as listener:
        print('listener starting')
        
        m = Manager()
        clients = m.dict()
        
        while True:
            print('accepting conexions')
            try:
                conn = listener.accept()
                print('connection accepted from', listener.last_accepted)
                client_info = conn.recv()
                usuarios.append(client_info['nombre'])
                pid = listener.last_accepted
                clients[pid] = client_info
                
                send_msg_all(pid, f"new client {pid}", clients)
                
                send_msg_all(pid, f"Los clientes conectados son: {usuarios}", clients)
                p = Process(target = serve_client, args = (conn, listener.last_accepted, clients, usuarios))
                p.start()
                
            except Exception as e:
                traceback.print_exc()
        print('end server')

if __name__ == '__main__':
    ip_address = '192.168.4.5'
    usuarios = []
    
    if len(sys.argv) > 1:
        ip_address = sys.argv[1]
    main(ip_address, usuarios)
