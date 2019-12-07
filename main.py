#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram.ext import Updater, CommandHandler
from telegram.ext.jobqueue import JobQueue
import datetime
import yaml
import re

with open('env_params.yml') as f:
    params = yaml.load(f, Loader=yaml.FullLoader)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class Days(object):
    MON, TUE, WED, THU, FRI, SAT, SUN = range(7)
    EVERY_DAY = tuple(range(7))
    WEEKDAYS = tuple(range(5))


TOKEN = params['token']


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text(
        f'Hi! I will tell you what did you ordered for today. '
        f'Type /order <name> with your name from the table and I will reply with your meal'
    )



def order(update, context):
    if datetime.datetime.today().weekday() > 4:
        update.message.reply_text(f"It's weekend!")
        return
    if not timeout.check(update, context):
        # fuck_you(update)
        return
    update.message.reply_text(f"Today's cleaner: {pq.get()}")


def participants(update, context):
    if not timeout.check(update, context):
        # fuck_you(update)
        return
    update.message.reply_text(f"Current participants are: {PARTICIPANTS}")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def table(update, context):
    message = update.message.text
    url = re.search("(?P<url>https?://[^\s]+)", message).group("url")

    update.message.reply_text(f"Table has been set for today!")



def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cleaner", cleaner))
    dp.add_handler(CommandHandler("participants", participants))
    dp.add_handler(CommandHandler("skip", skip))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    print(1)
    main()
