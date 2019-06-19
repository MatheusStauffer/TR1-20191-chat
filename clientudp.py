import socket 
import time
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
alias = input("Nickname:")
sock.sendto(alias.encode('utf-8'),("127.0.0.1",5002))
usuario=sock.recv(1024)
str_user=str(usuario,'utf-8')
sala = input("Digite a sala de chat que deseja entrar: ")

while True:
	if len(sala) > 1:
		sala = input("Digite um valor válido (1-5): ")
	elif(ord(sala) < 49 or ord(sala) > 54):
		sala = input("Digite um valor válido (1-5): ")
	else:
		break

sock.sendto(sala.encode(), ("127.0.0.1",5002))

message = input(alias + "-> ")

while message != 'q':
 if message != '':
  sock.sendto(message.encode(), ("127.0.0.1",5002))
  print("Mensagem enviada.")
  msg = sock.recv(1024)
  str_msg = str(msg)
  print(str_user + ": " + str_msg)
  message = input(alias + "-> ")
  time.sleep(0.2)
  sock.close()