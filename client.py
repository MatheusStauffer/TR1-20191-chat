import socket
import time

# definindo host e porta
host = '127.0.0.1'
port = 65000
addr = (host, port)

# instanciando um objeto socket e conectando com o host e porta definidos
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(addr)

# criando um alias para nickname
alias = input("Nickname: ")

# pegando mensagem do teclado
message = input(alias + "-> ")

# loop: para finalizar a conexão - i.e., para sair do while, enviar 'q'.
# enquanto for enviada uma mensagem vazia, o laço pede impõe novamente
# a escrita - pela linha "message = input(alias + "-> ")"
while message != 'q':
	if message != '':
		clientsocket.sendto(message.encode(), (addr))
		print("Mensagem enviada.")
	message = input(alias + "-> ")
	time.sleep(0.2)
clientsocket.close()