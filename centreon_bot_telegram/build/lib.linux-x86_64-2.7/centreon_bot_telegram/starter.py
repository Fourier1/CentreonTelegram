#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
    Implémentation de la proclamation de la bonne parole.
    Usage:
    from centreon_bot_telegram import proclamer
    App()
"""

# from daemon import runner
from telegram.ext import CommandHandler, CallbackQueryHandler

from setings import dispatcher, bot, chat_id, up
from centreon_telegram import echo, logger, error, buttton_menu, start, service_list, host_list, button_callback, \
    cancel, all_host_list, all_service_list

__all__ = ['service_list', 'host_list', 'button_callback', 'start', 'cancel', 'error', 'logger', 'all_service_list',
           'all_host_list', 'echo']


# class App():
#     def __init__(self):
#         self.stdin_path = '/dev/null'
#         self.stdout_path = '/dev/tty'
#         self.stderr_path = '/dev/tty'
#         self.pidfile_path = '/tmp/foo.pid'
#         self.pidfile_timeout = 5
#
#     def run(self):
def starters():
    """
    demarrage 
    :return: 
    """

    echo(bot=bot, update=chat_id)
    logger.info("Démarrer Centreon Bot ...")
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('menu', buttton_menu))
    dispatcher.add_handler(CommandHandler('cancel', cancel))
    dispatcher.add_handler(CommandHandler('host', host_list))
    dispatcher.add_handler(CommandHandler('allhost', all_host_list))
    dispatcher.add_handler(CommandHandler('allservice', all_service_list))
    dispatcher.add_handler(CommandHandler('service', service_list))
    dispatcher.add_error_handler(error)
    up.start_polling()
    up.idle()

if __name__ == '__main__':
    starters()

# app = App()
# daemon_runner = runner.DaemonRunner(app)
# daemon_runner.do_action()
