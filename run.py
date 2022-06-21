#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
import re
import datetime
import argparse
from pprint import pprint
from termcolor import colored

#-- 3rd party imports --#
from telegram import ChatAction
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
						  ConversationHandler)

#-- Local imports --#
from bot.bot import bot


# States of the ConversationHandler
MESSAGE_INCOME, CORR_INCORR, GET_CORRECT = range(3)


#The main object of the bot, see bot/bot.py to understand the implementation
bot = bot()


"""
	Function that responds to the /start command
"""
def start(bot, update, args):
	global BOT
	chat_id = update.message.chat_id
	if BOT.chats.user_has_data(chat_id):
		BOT.send_preset_message(chat_id, "start_known", BOT.chats.get_chat(chat_id)['name'])
	else:
		user_name = update.message.from_user.first_name
		data = {'name': user_name,
				'language': 'en',
				'current_state': BOT.state_machine['MessageHandler'],
				}
		BOT.chats.update_chat(chat_id, data, compulsory = True)
		BOT.send_preset_message(chat_id, "start_unknown_1", user_name)
		BOT.send_preset_message(chat_id, "start_unknown_2")
		BOT.send_preset_message(chat_id, "start_unknown_3")
	return MESSAGE_INCOME


"""
	Function that ends a conversation
"""
def done(bot, update):
	return ConversationHandler.END


def set_lang(bot, update):
	global BOT
	languages = ['Id','en']
	chat_id = update.message.chat_id
	text = update.message.text
	if len(text.split(' ')) > 1:
		lang = text.split(' ')[1]
		if lang in languages:
			BOT.chats.update_info(chat_id, 'language', lang, overwrite = True)
			BOT.send_preset_message(chat_id, "language_change_ok")
		else:
			BOT.send_preset_message(chat_id, "select_language")
	else:
		BOT.send_preset_message(chat_id, "wrong_lang_format")


"""
	Function that reads a regular message and decides which mechanism has to answer
"""
def ask(bot, update):
	global BOT
	chat_id = update.message.chat_id
	text = update.message.text
	message_id = update.message.message_id
	if BOT.chats.get_chat(chat_id)['logged'] & BOT.chats.token_has_expired(chat_id):
		BOT.chats.load()
	BOT.process_income_message(chat_id, text, message_id = message_id)
	return MESSAGE_INCOME

"""
	Function that manages the state machine
"""
def state_machine(bot, update):
	global BOT
	chat_id = update.message.chat_id
	message = update.message.text
	current_state = BOT.chats.get_chat(chat_id)['current_state']
	if current_state == BOT.state_machine['MessageHandler']:
		return ask(bot, update)
	elif current_state == BOT.state_machine['Wait_authorisation']:
		return authenticate(bot, update)


"""
	Main function, polls waiting for messages
"""
def main():
	global BOT

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--thread_log',
						action = 'store_true',
	                    help='Whether to log the threads info')
	args = parser.parse_args()

	BOT.load_components(thread_logging = bool(args.thread_log))
	print(colored("LOG: Todo inicializado", 'cyan'))
	# Create the Updater and pass it your bot's token.

	updater = Updater(BOT.bot_token)

	dp = updater.dispatcher

	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start, pass_args = True), CommandHandler('set_lang', set_lang),
					MessageHandler(filters = Filters.text, callback = state_machine)],
		states = {
			MESSAGE_INCOME: [MessageHandler(filters = Filters.text, callback = state_machine)],
		},
		fallbacks=[RegexHandler('^Done$', done)],
		allow_reentry = True #So users can use /login
	)

	dp.add_handler(conv_handler)

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

if __name__ == '__main__':
	main()
