import socket
import sys
import os
import time
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
address = ("127.0.0.1",5002)
sock.bind(address)

salas = [[] for _ in range(5)]

users = []

print("Conexão iniciada.")

try:
    while True:

     usuario,addr=sock.recvfrom(1024)
     str_user=usuario.decode('utf-8')
     sock.sendto(usuario,addr)


     sala,addr1=sock.recvfrom(1024)
     int_sala=int(sala)

     users.append((str_user, "127.0.0.1",5002))
     print(users)

     salas[int_sala-1].append(address)
     print(salas)
  
     print("Conectado com " + str_user, address)

    while True:
            # recebe mensagem. acho que o tamanho do buffer está ok
            msg,addr2 = sock.recv(1024)

            for address in salas[int_sala-1]:

                sock.sendto(msg, address)
                if(msg == 'exit'):

                     sock.close()
                     sys.exit(0)

                if not msg: break   

                str_msg = str(msg, 'utf-8')
                print(address, str_user + ':' , str_msg)
                    # quando o cliente se desconecta, mensagem indicativa e fechamento do socket
                    # respectivo
                print("Finalizando conexão do cliente " + str_user, address)
                clientsocket.close()
                sys.exit(0)
   
except Exception as ex:
 template = "An exception of type {0} occurred. Arguments:\n{1!r}"
 message = template.format(type(ex).__name__, ex.args)
 print(message)

	