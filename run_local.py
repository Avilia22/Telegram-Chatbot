#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
import argparse
from termcolor import colored

#-- Local imports --#
from bot.bot import bot


def main():
    CHAT_ID = None
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--thread_log',
    				action = 'store_true',
                    help='Whether to log the threads info')
    parser.add_argument('--chat_id',
                    required = False,
                    type = int,
                    default = 469557458,
                    help = "Chat_id for the conversation")
    parser.add_argument('--no_debug',
                        action = 'store_true',
                        required=False,
                        help="Prints debug information about queries")
    args = parser.parse_args()

    if args.chat_id:
        CHAT_ID = args.chat_id
    debug = not args.no_debug

    bot = bot(local = True, debug = debug)

    if args.thread_log: print(colored("LOG: Thread logging activo", 'cyan'))
    else: print(colored("LOG: Thread logging inactivo", 'cyan'))

    bot.load_components(thread_logging = bool(args.thread_log))

    print(colored("LOG:all initialized", 'cyan'))
    print(colored("INFO: Simulating conversation as user with chat_id {}".format(CHAT_ID), 'red'))
    print(colored("INFO: Type 'quit' to end conversation", 'red'))

    message = input('> ')
    while not message == 'quit':
        bot.process_income_message(CHAT_ID, message)
        message = input('> ')



if __name__ == '__main__':
    main()
