#Librerias Utilizadas
import socket
import threading

#especificamos direccion y puerto
host = '127.0.0.1'
port = 4343

#creacion del socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#datos de conexion e inicio del servidor
server.bind((host, port))
server.listen()
print(f" PenguServer iniciado {host}:{port}")

#listas para guardar datos de clientes y sus usuarios
clientes = []
usuarios = []

#envio de mensajes de usuarios a otros usuarios
def broadcast(message, yomismo):
    for client in clientes:
        if client != yomismo:
            client.send(message)

#Para desconexion del usuarios
def disconnected_client(client):
    index = clientes.index(client)
    usuario = usuarios[index]
    broadcast(f"PenguBot: [{usuario} ha abandonado el chat]".encode('utf-8'),client)
    clientes.remove(client)
    usuarios.remove(usuario)
    client.close()
    print(f"El usuario [{usuario}] se ha desconectado")


#mensaje de los usuarios
def handle_messages(client):
    while True:
        try:
            message = client.recv(128)
            broadcast(message,client)
        except:
            disconnected_client(client)
            break


#aceptacion de conexiones
def receive_connections():
    while True:
        client , address = server.accept()

        client.send("@username".encode("utf-8"))
        usuario = client.recv(128).decode("utf-8")

        clientes.append(client)
        usuarios.append(usuario)

        print(f"[{usuario}] se acaba de conectar al servidor {str(address)}")

        message = f"PenguBot: {usuario} se ha conectado!".encode("utf-8")
        broadcast(message, client)
        client.send("Ya estas conectado al PenguChat!".encode("utf-8"))

        thread = threading.Thread(target=handle_messages , args=(client,))
        thread.start()

receive_connections()




