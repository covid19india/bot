#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import os
from time import time
from src.entry import entry

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

BOT_TOKEN = os.environ["COVID_BOT_TOKEN"]
# How long the container exist
LIFESPAN = 3600

def main():
    """Run the bot."""  
      
    try:
        update_id = int(os.environ["UPDATE_ID"])
    except:
        update_id = 0

    start_time = int(time())

    bot = telegram.Bot(BOT_TOKEN)

    while True:
        try:
            for update in bot.get_updates(offset=update_id, timeout=60):
                update_id = update.update_id + 1
                entry(bot, update)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1
        if int(time()) - start_time > LIFESPAN:
            logging.info("Enough for the day! Passing on to next Meeseek")
            with open("/tmp/update_id", "w") as the_file:
                the_file.write(str(update_id))
            break

if __name__ == "__main__":
    main()
