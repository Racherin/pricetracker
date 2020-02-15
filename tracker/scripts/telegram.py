# coding: utf-8
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricetracker.settings")
django.setup()

import requests as requests
import random
import requests

url = "https://api.telegram.org/bot959432469:AAEDMEwG3xqh1lf2-7TBGzznkg75qsLQtZY/"


# create func that get chat id
def get_chat_id(update):
    chat_id = update['message']["chat"]["id"]
    return chat_id


# create function that get message text
def get_message_text(update):
    message_text = update["message"]["text"]
    return message_text


# create function that get last_update
def last_update(req):
    response = requests.get(req + "getUpdates")
    response = response.json()
    result = response["result"]
    total_updates = len(result) - 1
    return result[total_updates]  # get last record message update


# create function that let bot send message to user
def send_message(chat_id, message_text):
    params = {"chat_id": chat_id, "text": message_text, "parse_mode": 'html'}
    response = requests.post(url + "sendMessage", data=params)
    return response


# create main function for navigate or reply message back
def main():
    update_id = last_update(url)["update_id"]
    while True:
        update = last_update(url)
        if update_id == update["update_id"]:
            if get_message_text(update).lower() == "login" or get_message_text(update).lower() == "start":
                send_message(get_chat_id(update), "Alarm botuna hoşgeldiniz.")
            elif get_message_text(update).lower() == "/chatid":
                send_message(get_chat_id(update), get_chat_id(update))
            else:
                send_message(get_chat_id(update),
                             "<b>Geçersiz komut.</b>\nVaktinde Al Alarm Botunda verilebilcek tüm komutlar :\n/chatid : Size ait Chat ID numaranızı verir. \n/isactive : Telegram botunuzun aktif olup olmadığını gösterir.")
            update_id += 1


# call the function to make it reply
if __name__ == "__main__":
    main()
