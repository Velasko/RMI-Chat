# RMI-Chat
Chat coded in python using RMI

Programming language: Python 3.7.0

Used libraries:
	- json
	- time
	- socket
	- threading
	- tkinter
	- Pyro4

Pyro4 and tkinter might not come with your python version, depending on the operation system and/or python distribution.

The program consists in 4 files:
	- client.py - responsable for discovering the existing chats in the server and connecting the user to the chat room.
	- server.py - responsable for creating a 'dns server' to locate the uri and start the chat rooms.
	- user.py - contains the 'User' class which will create a GUI and interact with the chatroom via RMI.
	- chat.py - contains the 'Chat' class which manages the interations between the connected users.


In case no python 3.7 nor one of the libraries are installed in your machine, you may enter the 'server' and 'client' folders to execute the .exe files to verify it's functionalities.

The .exe versions were created using the pyinstall library.

In this version of the file server.exe, only 3 rooms are created.
