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