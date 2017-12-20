#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from telegram.ext import Updater
import telegram

# ----------------------------------------------------------------------------------------
BOT_TOKEN = '460850571:AAF9h-Q6XKLj_nqGmA7ciWoqm15jCH-1hZg'
URL_CENTREON = 'http://192.168.103.29/centreon/api/index.php'
AUTH_URL = URL_CENTREON + '?action=authenticate'
USERNAME_CENTREON = 'TelegramBot'
PASSWORD_CENTREON = 'tNrlcjcD'
# -----------------------------------------------------------------------------------------
up = Updater(token=BOT_TOKEN)
dispatcher = up.dispatcher
updater = Updater(BOT_TOKEN)
# Get the dispatcher to register handlers
dp = updater.dispatcher
# send mesage
bot = telegram.Bot(token=BOT_TOKEN)
bot_get_update = bot.get_updates()
chat_id = bot_get_update[-1].message.chat_id
user_name = bot_get_update[-1].message.from_user.first_name
