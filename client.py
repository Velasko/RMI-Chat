import user
import json
import socket as sk

def get_uris(server, port):
	'''Função que se conecta ao servidor \"dns\" de uri
	e descobre quais são os chats existentes'''
	socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
	socket.connect((server, port))

	socket.send('GET uri'.encode())

	serialized = socket.recv(4096).decode('utf-8')

	return json.loads(serialized)

def main(server='localhost', port=25500):

	#while para encontrar um nome de usuário válido
	while True:
		username = input('Username: ')

		if ':' not in username:
			break
		else:
			print("Nome de usuario não pode ter ':'. tente novamente")


	uris = get_uris(server, port)

	#while para selecionar uma sala de bate-papo válidada
	while True:
		print('Chats disponíveis:')
		for n, item in enumerate(uris):
			print(f"{n}: {item[0]}")

		selection = input("Pick a chat: ")

		try:
			uri = uris[int(selection)][1]
			break
		except (IndexError, ValueError):
			print(f"'{selection}' is not a valid chat, please, try again.")

	#A representação do usuário conectada ao bate-papo é instanciada
	u = user.User(uri, username)


if __name__ == '__main__':
	main()