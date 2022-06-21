
#-- General imports --#
from os import getenv
import requests
import json
import re
from time import time
from termcolor import colored

#-- 3rd party imports --#
from telegram import ChatAction



class bot(object):

	""" This object contains information and methods to manage the bot, and interact with
		its users.

	Attributes:
		local (:obj:`bool`): Indicates if it runs from Telegram or Locally
		name (:obj:`str`): Unique identifier for the bot
		bot_token (:obj:`str`): Token to access the bot
		message_handler : Object that handles messages
		delay (:obj:`int`): Number of seconds between scans on threads
		messages (:obj:`dict`): Object that contains the bot configuration messages
		state_machine (:obj:`dict`): Object that simplifies the state machine management
	"""
	def __init__(self, name = 'Fibot', local = False, debug = True):
		self.local = local
		self.debug = debug
		self.name = name
		self.bot_token = getenv('FibotTOKEN')
		self.message_handler = None
		self.delay = 60
		self.messages = {}
		self.state_machine = {
			'MessageHandler': '0',
			'Wait_authorisation': '1'
		}

	def log(self, text):
		print(colored("LOG: {}".format(text), 'cyan'))

	"""
		Loads the following components:
			chats: Loads the chats information from persistence
			message_handler: Enables it to send messages to users
			nlu: Loads the trained models
			qa: Loads the trained models
			messages: Loads the preset messages to memory
	"""
	def load_components(self, thread_logging = True):
		self.chats.load()
		self.log("Uploaded user database")
		if self.local: self.message_handler = Local_Message_handler(self.chats)
		else: self.message_handler = Message_handler(self.chats)

		self.qa.load()
		with open('./Data/messages.json', 'r') as fp:
			self.messages = json.load(fp)
		self.log("Mensajes predefinidos cargados")
		return

	"""
		Parameters:
			chat_id (:obj:`int`): chat id of the user to send the message to
			action (:obj:`str`): defines the action to send the user (default is typing)

		This function sends an action to the chat with chat_id (using ChatAction helper)
	"""
	def send_chat_action(self, chat_id, action = ChatAction.TYPING):
		self.message_handler.send_chat_action(chat_id, message, typing, reply_to)

	"""
		Parameters:
			chat_id (:obj:`int`): chat id of the user to send the message to
			message (:obj:`str`): content of the message to be sent
			typing (:obj:`bool`): value that defines whether to send typing action or not
			reply_to (:obj:`int` or None): If defined, it is the message_id of the message
				that will be replied to, else no message will be replied.
			parse_mode (:obj:`str`): The parse mode to use (normally Markdown or None)

		This function sends a message to the chat with chat_id with content text,
		and depending on the rest of the parameters it might do extra functionality.
	"""
	def send_message(self, chat_id, message, typing = False, reply_to = None, parse_mode = 'Markdown'):
		self.message_handler.send_message(chat_id, message, typing, reply_to, parse_mode)


	"""
		Parameters:
			chat_id (:obj:`str`): chat_id of the user to send the message to
			preset (:obj:`str`): the preset of the message to send
			param (:obj:`str` or None): the parameter of the messages

		This function sends a preset message to the user with user id.
		See /Data/messages.json to see the preset messages.
	"""
	def send_preset_message(self, chat_id, preset, param = None):
		user_lang = self.chats.get_chat(chat_id)['language']
		if param:
			message = self.messages[user_lang][preset].format(param)
		else:
			message = self.messages[user_lang][preset]
		if 'set_lang' in message: self.send_message(chat_id, message, typing=True, parse_mode = None)
		else: self.send_message(chat_id, message, typing=True)

	"""
		Parameters:
			chat_id (:obj:`str`): chat_id of the user that sent the messages
			message (:obj:`str`): text the user sent
			message_id (:obj:`int`): message_id of the message to reply to


		This function receives a message from a user and decides which mechanism is responsible
		for responding the message.
	"""
	def process_income_message(self, chat_id, message, message_id = None):
		user_language = self.chats.get_chat(chat_id)['language']
		now = time()
		response = self.qa.get_response(message, sender_id = chat_id, language = user_language, debug = self.debug)
		response = [i['text'] for i in response]
		self.send_message(chat_id, response, typing=True, reply_to = message_id, parse_mode = None)
