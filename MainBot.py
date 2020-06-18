import telebot
import config
import os
from Player import Player
import json
import JsonScenes
from telebot import types
from Scene import Scene
from Task import Task
import Level_1
import Level_2
import Level_3
import Level_4
import Level_5
import Level_6
import time
import Theory
import Theory_Handler
from flask import Flask, request

bot = telebot.TeleBot(config.Token, threaded=False)
global players
global Started
players = {}
current_handlers = {}
handlers_on_hold = {}
prev_types = {}
prev_parts = {}
prev_messages = {}
not_advancing_flags = {}
server = Flask(__name__)


@bot.message_handler(func=lambda message: check_player_in_dict(message.chat.id, "Theory"), content_types=['text'])
def handle_theory(message):
    global current_handlers
    global prev_parts
    global prev_types
    global prev_messages
    global handlers_on_hold
    global players
    current_handlers[message.chat.id].message = message
    if message.text == "Вернуться к игре":
        message = prev_messages[message.chat.id]
        prev_message = prev_messages[message.chat.id]
        if prev_message.text == "/start":
            send_welcome(prev_messages[message.chat.id])
            return
        if prev_message.text == "/Level1":
            switch_levels(prev_message)
            return
        elif prev_message.text == "/Level2":
            switch_levels(prev_message)
            return
        elif prev_message.text == "/Level3":
            switch_levels(prev_message)
            return
        elif prev_message.text == "/Level4":
            switch_levels(prev_message)
            return
        elif prev_message.text == "/Level5":
            switch_levels(prev_message)
            return
        elif prev_message.text == "/Level6":
            switch_levels(prev_message)
            return
        current_handlers[message.chat.id] = handlers_on_hold[message.chat.id]
        if prev_messages[message.chat.id].text == "Transition":
            current_handlers[message.chat.id].handle_start()
            return
        if prev_types[message.chat.id] == "Scene":
            players[message.chat.id].part_type = "Scene"
            current_handler = current_handlers[message.chat.id]
            current_handler.player.part_type = "Scene"
            current_handler.player.current_part = prev_parts[message.chat.id]
            current_handler.message = prev_messages[message.chat.id]
            current_handler.handle_scene()
            players[message.chat.id] = current_handler.player
            return
        else:
            players[message.chat.id].part_type = "Task"
            current_handler = current_handlers[message.chat.id]
            current_handler.player.part_type = "Task"
            current_handler.player.current_part = prev_parts[message.chat.id]
            current_handler.message = prev_messages[message.chat.id]
            current_handler.handle_task()
            players[message.chat.id] = current_handler.player
            return
    new_player = current_handlers[message.chat.id].handle_theory()
    players[message.chat.id] = new_player


@bot.message_handler(func=lambda message: message.text == "Теория" and check_player_for_theory(message.chat.id), content_types=['text'])
def theory(message):
    global handlers_on_hold
    global players
    global current_handlers
    handlers_on_hold[message.chat.id] = current_handlers[message.chat.id]
    current_handlers[message.chat.id] = Theory_Handler.Theory_Handler(bot, message)
    players[message.chat.id].part_type = "Theory"
    current_handlers[message.chat.id].handle_start()


def check_player_for_theory(id):
    global players
    return id in players


def go_to_level(message, handler):
    global current_handlers
    current_handlers[message.chat.id] = handler
    current_handlers[message.chat.id].handle_start()
    players[message.chat.id] = current_handlers[message.chat.id].player
    prev_messages[message.chat.id].text = message.text
    return


def generate_markup_for_theory(answers):
    markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
    for answer in answers:
        markup.add(answers)
    markup.add("Вернуться к игре")
    return markup


@bot.message_handler(commands=['test'])
def get_ids(message):
    path = os.getcwd() + "/Illustrations"#+ "/Theory"
    for file in os.listdir(path):
        f = open(path + "\\" + file, 'rb')
        msg = bot.send_photo(message.chat.id, f)
        bot.send_message(message.chat.id, msg.photo[2].file_id, reply_to_message_id=msg.message_id)



        # bot.send_message(message.chat.id, dir)
        # for subdir in os.listdir(path + "\\" + dir):
        #     bot.send_message(message.chat.id, subdir)
        #     for file in os.listdir(path + "\\"+ dir + "\\"+ subdir):
        #         f = open(path + "\\"+ dir + "\\"+ subdir + "\\" + file, 'rb')
        #         msg = bot.send_photo(message.chat.id, f)
        #         bot.send_message(message.chat.id, msg.photo[2].file_id, reply_to_message_id=msg.message_id)


@bot.message_handler(commands=['start', 'restart'])
def send_welcome(message):
    global players
    global current_handlers
    global prev_types
    global prev_parts
    global prev_messages
    current_handlers[message.chat.id] = Level_1.Level_1_Handler(message.chat.id, message, bot)
    players[message.chat.id] = current_handlers[message.chat.id].player
    current_handlers[message.chat.id].handle_start()
    prev_messages[message.chat.id] = message
    prev_types[message.chat.id] = players[message.chat.id].part_type
    prev_parts[message.chat.id] = players[message.chat.id].current_part


@bot.message_handler(commands=["Level1", "Level2", "Level3", "Level4", "Level5", "Level6"])
def switch_levels(message):
    global current_handlers
    if not check_player_for_theory(message.chat.id):
        return
    if message.text == "/Level1":
        go_to_level(message, Level_1.Level_1_Handler(message.chat.id, message, bot))
    elif message.text == "/Level2":
        go_to_level(message, Level_2.Level_2_Handler(message.chat.id, message, bot))
    elif message.text == "/Level3":
        go_to_level(message, Level_3.Level_3_Handler(message.chat.id, message, bot))
    elif message.text == "/Level4":
        go_to_level(message, Level_4.Level_4_Handler(message.chat.id, message, bot))
    elif message.text == "/Level5":
        go_to_level(message, Level_5.Level_5_Handler(message.chat.id, message, bot))
    elif message.text == "/Level6":
        go_to_level(message, Level_6.Level_6_Handler(message.chat.id, message, bot))


def check_player_in_dict(id, type):
    if id not in players:
        return False
    return id in players and players[id].part_type == type


# Менять при смене уровня player в дикте игроков, иначе баг (18.06.20, не пофикшено)
@bot.message_handler(func=lambda message: check_player_in_dict(message.chat.id, "Scene"), content_types=['text'])
def handle_scene(message):
    global current_handlers
    global prev_parts
    global prev_messages
    global prev_types
    global not_advancing_flags
    #Менять сообщение сцены только если поменялся тип или номер данного куска

    #Менять при смене хэндлера вручную все prev (костыль)
    player = players[message.chat.id]
    if player.current_part.check_advancing(message.text) or player.current_part.get_without_answers_flag():
        prev_types[message.chat.id] = players[message.chat.id].part_type
        prev_parts[message.chat.id] = players[message.chat.id].current_part
        prev_messages[message.chat.id] = message
    current_handlers[message.chat.id].message = message
    new_player, transition = current_handlers[message.chat.id].handle_scene()
    players[message.chat.id] = new_player
    if transition == 2:
        current_handlers[message.chat.id] = Level_2.Level_2_Handler(message.chat.id, message, bot)
        current_handlers[message.chat.id].handle_start()
        prev_parts[message.chat.id] = current_handlers[message.chat.id].player.current_part
        prev_types[message.chat.id] = current_handlers[message.chat.id].player.part_type
        prev_messages[message.chat.id].text = "/Level2"
        players[message.chat.id] = current_handlers[message.chat.id].player
    elif transition == 3:
        current_handlers[message.chat.id] = Level_3.Level_3_Handler(message.chat.id, message, bot)
        current_handlers[message.chat.id].handle_start()
        prev_parts[message.chat.id] = current_handlers[message.chat.id].player.current_part
        prev_types[message.chat.id] = current_handlers[message.chat.id].player.part_type
        prev_messages[message.chat.id].text = "/Level3"
        players[message.chat.id] = current_handlers[message.chat.id].player
    elif transition == 4:
        current_handlers[message.chat.id] = Level_4.Level_4_Handler(message.chat.id, message, bot)
        current_handlers[message.chat.id].handle_start()
        prev_parts[message.chat.id] = current_handlers[message.chat.id].player.current_part
        prev_types[message.chat.id] = current_handlers[message.chat.id].player.part_type
        prev_messages[message.chat.id].text = "/Level4"
        players[message.chat.id] = current_handlers[message.chat.id].player
    elif transition == 5:
        current_handlers[message.chat.id] = Level_5.Level_5_Handler(message.chat.id, message, bot)
        current_handlers[message.chat.id].handle_start()
        prev_parts[message.chat.id] = current_handlers[message.chat.id].player.current_part
        prev_types[message.chat.id] = current_handlers[message.chat.id].player.part_type
        prev_messages[message.chat.id].text = "/Level5"
        players[message.chat.id] = current_handlers[message.chat.id].player
    elif transition == 6:
        current_handlers[message.chat.id] = Level_6.Level_6_Handler(message.chat.id, message, bot)
        current_handlers[message.chat.id].handle_start()
        prev_parts[message.chat.id] = current_handlers[message.chat.id].player.current_part
        prev_types[message.chat.id] = current_handlers[message.chat.id].player.part_type
        prev_messages[message.chat.id].text = "/Level6"
        players[message.chat.id] = current_handlers[message.chat.id].player


@bot.message_handler(func=lambda message: check_player_in_dict(message.chat.id, "Task"), content_types=["text"])
def handle_task(message):
    global current_handlers
    global prev_parts
    global prev_messages
    global prev_types
    global not_advancing_flags
    player = players[message.chat.id]
    if player.current_part.check_advancing(message.text) or player.current_part.get_without_answers_flag():
        prev_types[message.chat.id] = players[message.chat.id].part_type
        prev_parts[message.chat.id] = players[message.chat.id].current_part
        prev_messages[message.chat.id] = message
    current_handlers[message.chat.id].message = message
    new_player, transition = current_handlers[message.chat.id].handle_task()
    players[message.chat.id] = new_player
    if transition == 2:
        current_handlers[message.chat.id] = Level_2.Level_2_Handler(message.chat.id, message, bot)
        current_handlers[message.chat.id].handle_start()
        prev_parts[message.chat.id] = current_handlers[message.chat.id].player.current_part
        prev_types[message.chat.id] = current_handlers[message.chat.id].player.part_type
        prev_messages[message.chat.id].text = "/Level2"
        players[message.chat.id] = current_handlers[message.chat.id].player
    elif transition == 3:
        current_handlers[message.chat.id] = Level_3.Level_3_Handler(message.chat.id, message, bot)
        current_handlers[message.chat.id].handle_start()
        prev_parts[message.chat.id] = current_handlers[message.chat.id].player.current_part
        prev_types[message.chat.id] = current_handlers[message.chat.id].player.part_type
        prev_messages[message.chat.id].text = "/Level3"
        players[message.chat.id] = current_handlers[message.chat.id].player
    elif transition == 4:
        current_handlers[message.chat.id] = Level_4.Level_4_Handler(message.chat.id, message, bot)
        current_handlers[message.chat.id].handle_start()
        prev_parts[message.chat.id] = current_handlers[message.chat.id].player.current_part
        prev_types[message.chat.id] = current_handlers[message.chat.id].player.part_type
        prev_messages[message.chat.id].text = "/Level4"
        players[message.chat.id] = current_handlers[message.chat.id].player
    elif transition == 5:
        current_handlers[message.chat.id] = Level_5.Level_5_Handler(message.chat.id, message, bot)
        current_handlers[message.chat.id].handle_start()
        prev_parts[message.chat.id] = current_handlers[message.chat.id].player.current_part
        prev_types[message.chat.id] = current_handlers[message.chat.id].player.part_type
        prev_messages[message.chat.id] = "/Level5"
        players[message.chat.id] = current_handlers[message.chat.id].player
    elif transition == 6:
        current_handlers[message.chat.id] = Level_6.Level_6_Handler(message.chat.id, message, bot)
        current_handlers[message.chat.id].handle_start()
        prev_parts[message.chat.id] = current_handlers[message.chat.id].player.current_part
        prev_types[message.chat.id] = current_handlers[message.chat.id].player.part_type
        prev_messages[message.chat.id] = "/Level6"
        players[message.chat.id] = current_handlers[message.chat.id].player


@server.route('/bot', methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://divinely-inspired-project.herokuapp.com/bot')
    return "!", 200


server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)))


# bot.polling(none_stop=True)
