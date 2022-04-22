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
    print()
