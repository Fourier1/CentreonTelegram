#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import logging
import telegram
import requests
import json
from emoji import emojize
from telegram import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction

from setings import chat_id, user_name, AUTH_URL, USERNAME_CENTREON, PASSWORD_CENTREON, URL_CENTREON

# les Debug
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def echo(bot, update):
    """
    Affichier le message de bienvenu su le bot telegram
    :param bot: 
    :param update: 
    :return: 
    """
    mesg = '* %s * Bienvenue sur Bot Telegram centreon \n Entrer /start pour demerer le Bot !' % user_name
    bot.send_message(chat_id=chat_id, text=mesg, parse_mode=telegram.ParseMode.MARKDOWN)


def get_token_contreon():
    """
    Recuperer le Token de centreon a chaque fois qu'il change
    :return: Token
    """
    request = requests.post(AUTH_URL, data={'username': USERNAME_CENTREON, 'password': PASSWORD_CENTREON})
    centreon_token = request.json()['authToken']
    return centreon_token


def build_menu(buttons, n_cols):
    """
    Creation du menu de 2 colones et en finction des serveurs n otifiers
    :param buttons: le bouton
    :param n_cols: nombre de colone
    :return: menu
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    return menu


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" cause d\'erreur "%s"', update, error)


def cancel(bot, update):
    """
    Fonction d'arret du chat avec le bot
    :param bot: 
    :param update: 
    :return: 
    """
    user = update.message.from_user
    logger.info("l\'utilisateur %s a quitter la conversation.", user.first_name)
    update.message.reply_text("Bye! J'espère qu'on pourra reparler un jour.", reply_markup=ReplyKeyboardRemove())


def buttton_menu(bot, update):
    """
    Menu Bouton avec des actions definies
    :param bot: 
    :param update: 
    :return: 
    """
    hst = telegram.KeyboardButton(text="/host", request_contact=False)
    sevc = telegram.KeyboardButton(text="/service", request_contact=False)
    canl = telegram.KeyboardButton(text="/cancel", request_contact=False)
    all_hosts = telegram.KeyboardButton(text="/allhost", request_contact=False)
    all_services = telegram.KeyboardButton(text="/allservice", request_contact=False)
    custom_keyboard = [[hst, sevc, canl, all_hosts, all_services]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text("Vous avez un racourci des boutons juste en dessous !", reply_markup=reply_markup)


def host_list(bot, update):
    """
    afficher la liste des hots aillant des problems 
    :param bot: 
    :param update: 
    :return: 
    """
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    headers = {'centreon-auth-token': get_token_contreon()}
    requete = requests.get(
        URL_CENTREON + '?object=centreon_realtime_hosts&action=list&status=critical&viewType=unhandled',
        headers=headers)
    host_list = requete.json()
    if not host_list:
        msg = "Aucun host trouvé avec problème non géré\n"
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        return
    msg = "Host trouvé avec problème non géré:\n"
    button_list = list()
    for host in host_list:
        button_list.append(InlineKeyboardButton(text=host['name'],
                                                callback_data='{"P":' + host['id'] + ',"H":"' + host['name'] + '"}'))
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup)


def service_list(bot, update):
    """
    Afficher la liste des services aillant un problem
    :param bot: 
    :param update: 
    :return: 
    """
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    headers = {'centreon-auth-token': get_token_contreon()}
    requets = requests.get(URL_CENTREON + '?object=centreon_realtime_services&action=list&viewType=unhandled',
                           headers=headers)
    service_list = requets.json()
    if not service_list:
        msg = "Aucun service trouvé avec problème non géré\n"
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        return
    msg = "Service trouvé avec problème non géré :\n"
    button_list = list()
    for service in service_list:
        button_list.append(InlineKeyboardButton(text=service['name'] + '/' + service['description'],
                                                callback_data='{"P":' + service['service_id'] + ',"H":"' + service[
                                                    'name'] + '","S":"' + service['description'] + '"}'))
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup)


def button_callback(bot, update):
    """
    Rappel de boutons 
    :param bot: 
    :param update: 
    :return: 
    """
    query = update.callback_query
    bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.TYPING)
    Cdata = json.loads(query.data)
    if not Cdata.has_key('S'):
        headers = {'centreon-auth-token': get_token_contreon(), 'content-type': 'application/json'}
        pollerid = Cdata['P']
        command = 'ACKNOWLEDGE_HOST_PROBLEM;%s;%s;%s;%s;%s;%s' % (
            Cdata['H'], 2, 1, 1, update.callback_query.from_user.username, "Aquitter avec le Bot")

        payload = {"commands": [{"poller_id": str(pollerid), "command": command}]}
        r = requests.post(URL_CENTREON + '?object=centreon_monitoring_externalcmd&action=send', headers=headers,
                          json=payload)

        if r.status_code == 200:
            bot.send_message(chat_id=query.message.chat_id, text=' Aquittement fait pour ' + Cdata['H'])
        else:
            bot.send_message(chat_id=query.message.chat_id, text=' Une erreur s\'est produite pendant l\'action')
    else:
        headers = {'centreon-auth-token': get_token_contreon(), 'content-type': 'application/json'}
        pollerid = Cdata['P']
        command = 'ACKNOWLEDGE_SVC_PROBLEM;%s;%s;%s;%s;%s;%s;%s' % (
            Cdata['H'], Cdata['S'], 2, 1, 1, update.callback_query.from_user.username, "Aquitter avec le Bot")
        payload = {"commands": [{"poller_id": str(pollerid), "command": command}]}
        r = requests.post(URL_CENTREON + '?object=centreon_monitoring_externalcmd&action=send', headers=headers,
                          json=payload)
        if r.status_code == 200:
            bot.send_message(chat_id=query.message.chat_id,
                             text=' Aquittement fait pour ' + Cdata['H'] + '/' + Cdata['S'])
        else:
            bot.send_message(chat_id=query.message.chat_id, text=' Une erreur s\'est produite pendant l\'action')


def all_host_list(bot, update):
    """
    Afficher la liste de tous les hosts enregistrer sur centreon
    :param bot: 
    :param update: 
    :return: 
    """
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    headers = {'centreon-auth-token': get_token_contreon(), 'Content-Type': "application/json"}
    requete = requests.get(URL_CENTREON + '?object=centreon_realtime_hosts&action=list', headers=headers)

    all_host_lists = requete.json()
    if not all_host_lists:
        message = "Pas d'Hots enregistrer sur centreon !"
        bot.send_message(chat_id=update.message.chat_id, text=message)
        return
    message = "Liste des Hosts enregistrer sur centreon :"
    all_host = list()
    for host in all_host_lists:
        all_host.append(InlineKeyboardButton(text=host['name'],
                                             callback_data='{"P":' + host['id'] + ',"H":"' + host['name'] + '"}'))
    reply_markup = InlineKeyboardMarkup(build_menu(all_host, n_cols=2))
    bot.send_message(chat_id=update.message.chat_id, text=message, reply_markup=reply_markup)


def all_service_list(bot, update):
    """
    Afficher la liste des hosts aillant un problem
    :param bot: 
    :param update: 
    :return: 
    """
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    headers = {'centreon-auth-token': get_token_contreon(), 'Content-Type': "application/json"}
    requets = requests.get(URL_CENTREON + '?object=centreon_realtime_services&action=list',
                           headers=headers)
    all_service_lists = requets.json()
    print "liste service : ", all_service_lists
    # if not service_list:
    #     msg = "Aucun service trouvé\n"
    #     bot.send_message(chat_id=update.message.chat_id, text=msg)
    #     return
    # msg = "Service trouvé :\n"
    # all_services = list()
    # for service in all_service_lists:
    #     all_services.append(InlineKeyboardButton(text=service['name'] + '/' + service['description'],
    #                                              callback_data='{"P":' + service['service_id'] + ',"H":"' + service[
    #                                                  'name'] + '","S":"' + service['description'] + '"}'))
    # reply_markup = InlineKeyboardMarkup(build_menu(all_services, n_cols=2))
    # bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup)


def start(bot, update):
    """
    Démarage du bote centreon 
    :param bot: le bote
    :param update: le mises ajours du bot
    :return: 
    """
    msg = emojize(":information_source:", use_aliases=True) + " Salut {user_name}!\n"
    msg += "Je suis *{bot_name}*\n"
    msg += "mon role est de reconnaitre les probelmes de [Centreon](http://10.254.2.50/centreon/) \n"
    msg += "que voulez-vous faire ? \n"
    msg += "cliquer sur un bouton en fonction de l'action de votre chois\n"
    msg += "/host (s) - *HOSTS* : hots avec un probleme non gere\n"
    msg += "/allhost (s) - *HOSTS* : liste des hots present sur centreon\n"
    msg += "/allservice (s) - *SERVICES* : liste des services present sur centreon\n"
    msg += "/service (s) - *SERVICE* : services avec un probleme non gere\n"
    msg += "/cancel - *CANCEL* : quiter la conversation\n"
    msg += "/menu - *MENU DE BOUTON* : afficher les bouton\n"
    bot.send_message(chat_id=update.message.chat_id, text=msg.format(user_name=update.message.from_user.first_name,
                                                                     bot_name=bot.first_name), parse_mode='Markdown')
