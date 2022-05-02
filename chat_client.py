"""
PROGRAMACIÓN DISTRIBUIDA
------------------------
Práctica 3: Chat

Autoras: Claudia Casado Poyatos
         Natalia García Domínguez
         Olga Rodríguez Acevedo
"""

def main(server_address, info):
    print("**************Intentando conectar**************")
    with Client(address = (server_address, 6000), authkey = b'secret password server') as conn:
        fn = sys.fileno()
        cl = Process(target = client_listener, args = (info, conn, fn, ))
        cl.start()
        sleep(1)
        conn.send(info)
        connected = True
        while connected:
            command = input('Escribe "lista" si quieres conocer los usuarios en linea o \n "chat" si quieres iniciar una conversacion \n')
            if command == "lista":
                conn.send((command, 0, 0))
                list_clients_connected = conn.recv()
                print("Los usuarios conectados son: list_clients_connected)
            elif command == "chat":
                user = input('¿Con quién quieres hablar? ')
              conn.send((command,user,info))
              info_user == conn.secv()
              if info_user ==[]:
                print("Nombre incorrecto. Vuelve a intentarlo.")
              else:
                connected= False
                conn.close()
                cl.terminate()
                connection1 = Process(traget=connection, args =(info,info_user,fn,))
                conection1.start()
      elif command == "salir":
              connected = False
              conn.close()
      elif command == "ACEPTO":
              info_client = conn.recv()
              connected= False
              conn.close()
              cl.terminate()
              connection_emisor = Process(target=emisor_connection, args=(info_client, fn,))
              connection_emisor.start()
   cl.terminate()
if __name__ =='__main__':
     server_address = '192.168.9.6'
     client_address = ''
     client_port = 6001
              
     nombre= input(¿Cual es tu nombre? ')
     if len(sys.argv) >1:
           client_port = int(sys.argv[1])
     if len(sys.argv) >2:
           client_address= sys.argv[2]
     if len(sys.argv) >3:
            server_address= sys.argv[3]
     info) {'nombre': nombre, 'address': client_address, 'port': client_port, 'authkey':b'secret client server'}
           main(server_address, info)
              
