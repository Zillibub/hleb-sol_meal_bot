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
from current_order import CurrentOrder

with open('env_params.yml') as f:
    params = yaml.load(f, Loader=yaml.FullLoader)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = params['token']

co = CurrentOrder()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text(
        f'Hi! I will tell you what did you ordered for today. '
        f'Type /order <name> with your name from the table and I will reply with your meal'
    )


def order(update, context):
    message = update.message.text
    try:
        o = co.instance.get_order(message.split(' ')[1])
    except Exception as e:
        update.message.reply_text(f"Error: {e}")
        return
    update.message.reply_text(f"Your order is: {o}")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def table(update, context):
    message = update.message.text

    url = re.search("(?P<url>https?://[^\s]+)", message).group("url")

    try:
        co.instance.set_table(url)
    except Exception as e:
        update.message.reply_text(f"Could not part table, error: {e}")
        return


    chat_id = update.message.chat_id
    job_queue: JobQueue = context.job_queue

    new_job = job_queue.run_once(
        callback=clean_table,
        when=datetime.time(hour=23, minute=29),
        context=chat_id
    )
    context.chat_data['job'] = new_job

    update.message.reply_text(f"Table has been set for today! It will be deleted at midnight")


def clean_table(_):
    """
    Setting current table to None
    :param _:  context, useless here
    :return:
    """
    co.instance.clear_table()


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
    dp.add_handler(CommandHandler("order", order))
    dp.add_handler(CommandHandler("table", table))

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
