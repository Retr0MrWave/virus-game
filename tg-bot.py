#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

import VirusGame as vg
games_dict = {"":""}

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if len(context.args) != 2:
        update.message.reply_text("You messed up the parameters. I need two integers, seperated by a space. It's not that hard")
        return
    try:
        w = int(context.args[0])
        h = int(context.args[1])
    except (ValueError):
        update.message.reply_text("You messed up the parameters. I need two integers, seperated by a space. It's not that hard")
        return
    games_dict.pop(update.message.chat_id, None)
    games_dict[update.message.chat_id] = [vg.Game(w, h), 1, 3]
    update.message.reply_text("```\n" + games_dict[update.message.chat_id][0].getString() + "\n```", parse_mode="MarkdownV2")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Of course I didn\'t bother putting this in')


def move1(update: Update, context: CallbackContext) -> None:
    id = update.message.chat_id
    try:
        games_dict[id]
    except KeyError:
        update.message.reply_text("I\'m afraid you didn't start a game yet")
        return
    if games_dict[id][1] == 2:
        update.message.reply_text("It\'s not your turn")
        return
    try:
        move = [int(context.args[0]), int(context.args[1])]
    except (ValueError, IndexError):
        update.message.reply_text("You messed up the parameters. I need two integers, seperated by a space. It's not that hard")
        return
    if not(games_dict[id][0].makeMove(1, move.copy())):
        update.message.reply_text("Invalid move")
        return
    update.message.reply_text("```\n" + games_dict[update.message.chat_id][0].getString() + "\n```", parse_mode="MarkdownV2")
    games_dict[id][2] -= 1
    if games_dict[id][2] == 0:
        if games_dict[id][0].checkGameEnd(2):
            update.message.reply_text("Player 1 won")
            games_dict.pop(update.message.chat_id, None)
            return
        games_dict[id][2] = 3
        games_dict[id][1] = 2
    else:
        if games_dict[id][0].checkGameEnd(1):
            update.message.reply_text("Player 2 won")
            games_dict.pop(update.message.chat_id, None)
            return
            
def move2(update: Update, context: CallbackContext) -> None:
    id = update.message.chat_id
    try:
        games_dict[id]
    except KeyError:
        update.message.reply_text("I\'m afraid you didn't start a game yet")
        return
    if games_dict[id][1] == 1:
        update.message.reply_text("It\'s not your turn")
        return
    try:
        move = [int(context.args[0]), int(context.args[1])]
    except (ValueError, IndexError):
        update.message.reply_text("You messed up the parameters. I need two integers, seperated by a space. It's not that hard")
        return
    if not(games_dict[id][0].makeMove(2, move.copy())):
        update.message.reply_text("Invalid move")
        return
    update.message.reply_text("```\n" + games_dict[update.message.chat_id][0].getString() + "\n```", parse_mode="MarkdownV2")
    games_dict[id][2] -= 1
    if games_dict[id][2] == 0:
        if games_dict[id][0].checkGameEnd(1):
            update.message.reply_text("Player 2 won")
            games_dict.pop(update.message.chat_id, None)
            return
        games_dict[id][2] = 3
        games_dict[id][1] = 1
    else:
        if games_dict[id][0].checkGameEnd(2):
            update.message.reply_text("Player 1 won")
            games_dict.pop(update.message.chat_id, None)
            return


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    tokenfile = open("token.txt", 'r')
    token = tokenfile.readline()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start, pass_args=True))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("move1", move1, pass_args=True))
    dispatcher.add_handler(CommandHandler("move2", move2, pass_args=True))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()