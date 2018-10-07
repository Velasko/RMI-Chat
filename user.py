import Pyro4
import tkinter
import threading

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class User():
	def __init__(self, uri, username):
		"""The instantiation of this class requires:
			- uri : str - uri to connect to chat.
			- username : str - how it shall be displayed for the participants in the chat."""

		self.chat = Pyro4.Proxy(uri)
		self._username = username

		#Creating window
		self.top = tkinter.Tk()
		self.top.title(f"{self.username}'s chat")# at {self.chat.name}")

		messages_frame = tkinter.Frame(self.top)

		#Creating display messages fields
		scrollbar = tkinter.Scrollbar(messages_frame)
		self.messages = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)

		scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
		self.messages.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
		self.messages.pack()
		messages_frame.pack()

		#Creating input text field
		self.my_msg = tkinter.StringVar()
		# my_msg.set("Type your messages here.")
		entry_field = tkinter.Entry(self.top, textvariable=self.my_msg)
		entry_field.bind("<Return>", self.send_message)
		entry_field.pack()

		send_button = tkinter.Button(self.top, text="Send", command=self.send_message)
		send_button.pack()

		#On closing
		self.top.protocol("WM_DELETE_WINDOW", self.disconnect)

		self.connect()

		try:
			tkinter.mainloop()
		except Exception as e:
			print(e)
			self.disconnect()
		
	def connect(self):
		"""Method to connect and register at the chat"""

		print('Connecting to server')

		#Creating daemon so the chat can access this object.
		daemon = Pyro4.Daemon()
		self._my_uri = daemon.register(self)

		self.t = threading.Thread(target=daemon.requestLoop)
		self.t.daemon = True
		self.t.start()

		messages = self.chat.connect(self.my_uri)

		#in case the connection is refused:
		if isinstance(messages, bool) and not messages:
			raise ValueError(f"Username {self.username} already taken")

		print('Connected')

		#if the connection is accepted, the last 20 messages are sent
		#those messages will now be printed.
		for message in messages:
			self.incoming_message(message)

	def disconnect(self):
		"""This method closes the window and clears the username in the chat."""
		self.top.quit()
		self.chat.disconnect(self.my_uri)
		print('Disconnected')

	def send_message(self, message=None):
		#Getting message from window, clearing then sending to server
		message = self.my_msg.get()
		self.my_msg.set("")
		message = f"""{self.username}: {message}"""

		self.chat.send_message(message, self.my_uri)

		#as the chat can't call methods from this object when it's called,
		#it must be printed by itself
		self.incoming_message(message)

	def incoming_message(self, message):
		#Recieving a message -> displaying at window.
		self.messages.insert(tkinter.END, message)

	def __eq__(self, other):
		return self.username == other.username

	def __str__(self):
		return self._username

	def __repr__(self):
		return self._username

	@property
	def username(self):
		return self._username

	@property
	def my_uri(self):
		return self._my_uri
	
	