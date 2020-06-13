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

bot = telebot.TeleBot(config.Token)
global players
global Started
Started = False
players = {}
global current_nandler
global handler_on_hold
global prev_type
global prev_part
global prev_message
global not_advancing
not_advancing = False
server = Flask(__name__)

@bot.message_handler(func=lambda message: check_player_in_dict(message.chat.id, "Theory"), content_types=['text'])
def handle_theory(message):
    global current_nandler
    global prev_part
    global prev_type
    global prev_message
    global handler_on_hold
    global players
    global Started
    global not_advancing
    current_nandler.message = message
    if message.text == "Вернуться к игре":
        message = prev_message
        if prev_message.text == "/start":
            Started = False
            send_welcome(prev_message)
        current_nandler = handler_on_hold
        if prev_message.text == "Transition":
            current_nandler.handle_start()
            return
        if prev_type == "Scene":
            not_advancing = False
            players[message.chat.id].part_type = "Scene"
            current_nandler.player.part_type = "Scene"
            current_nandler.player.current_part = prev_part
            current_nandler.message = prev_message
            current_nandler.handle_scene()
            players[message.chat.id] = current_nandler.player
            return
        else:
            not_advancing = False
            players[message.chat.id].part_type = "Task"
            current_nandler.player.part_type = "Task"
            current_nandler.player.current_part = prev_part
            current_nandler.message = prev_message
            current_nandler.handle_task()
            players[message.chat.id] = current_nandler.player
            return
    new_player = current_nandler.handle_theory()
    players[message.chat.id] = new_player

@bot.message_handler(func=lambda message: message.text == "Теория")
def theory(message):
    global handler_on_hold
    global players
    global current_nandler
    type_on_hold = players[message.chat.id].part_type
    handler_on_hold = current_nandler
    current_nandler = Theory_Handler.Theory_Handler(bot, message)
    players[message.chat.id].part_type = "Theory"
    current_nandler.handle_start()

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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global Started
    global players
    global current_nandler
    global prev_type
    global prev_part
    global prev_message
    text_directory = os.getcwd() + "/JsonScenes"
    if Started == False:
        Started = True
        current_nandler = Level_1.Level_1_Handler(message.chat.id, message, bot)
        players[message.chat.id] = current_nandler.player
        current_nandler.handle_start()
        prev_message = message
        prev_type = players[message.chat.id].part_type
        prev_part = players[message.chat.id].current_part
    else:
        bot.send_message(message.chat.id, "Твоё приключение уже началось")

@bot.message_handler(commands=["Level1", "Level2", "Level3", "Level4", "Level5", "Level6"])
def go_to_level(message):
    global  current_nandler
    if message.text == "/Level1":
        current_nandler = Level_1.Level_1_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        players[message.chat.id] = current_nandler.player
        prev_message.text = "Transition"
    elif message.text == "/Level2":
        current_nandler = Level_2.Level_2_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        players[message.chat.id] = current_nandler.player
        prev_message.text = "Transition"
    elif message.text == "/Level3":
        current_nandler = Level_3.Level_3_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        players[message.chat.id] = current_nandler.player
        prev_message.text = "Transition"
    elif message.text == "/Level4":
        current_nandler = Level_4.Level_4_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        players[message.chat.id] = current_nandler.player
        prev_message.text = "Transition"
    elif message.text == "/Level5":
        current_nandler = Level_5.Level_5_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        players[message.chat.id] = current_nandler.player
        prev_message.text = "Transition"
    elif message.text == "/Level6":
        current_nandler = Level_6.Level_6_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        players[message.chat.id] = current_nandler.player
        prev_message.text = "Transition"


def check_player_in_dict(id, type):
    if id not in players:
        return False
    return id in players and players[id].part_type == type

@bot.message_handler(func=lambda message: check_player_in_dict(message.chat.id, "Scene"), content_types=['text'])
def handle_scene(message):
    global current_nandler
    global prev_part
    global prev_message
    global prev_type
    global not_advancing
    #Менять сообщение сцены только если поменялся тип или номер данного куска

    #Менять при смене хэндлера вручную все prev (костыль)
    player = players[message.chat.id]
    if not not_advancing and player.current_part.check_advancing(message.text):
        prev_type = players[message.chat.id].part_type
        prev_part = players[message.chat.id].current_part
        prev_message = message
    else:
        not_advancing = True
    current_nandler.message = message
    new_player, transition = current_nandler.handle_scene()
    players[message.chat.id] = new_player
    if transition == 2:
        current_nandler = Level_2.Level_2_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        prev_part = current_nandler.player.current_part
        prev_type = current_nandler.player.part_type
        prev_message.text = "Transition"
    elif transition == 3:
        current_nandler = Level_3.Level_3_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        prev_part = current_nandler.player.current_part
        prev_type = current_nandler.player.part_type
        prev_message.text = "Transition"
    elif transition == 4:
        current_nandler = Level_4.Level_4_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        prev_part = current_nandler.player.current_part
        prev_type = current_nandler.player.part_type
        prev_message.text = "Transition"
    elif transition == 5:
        current_nandler = Level_5.Level_5_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        prev_part = current_nandler.player.current_part
        prev_type = current_nandler.player.part_type
        prev_message.text = "Transition"
    elif transition == 6:
        current_nandler = Level_6.Level_6_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        prev_part = current_nandler.player.current_part
        prev_type = current_nandler.player.part_type
        prev_message.text = "Transition"

@bot.message_handler(func=lambda message: check_player_in_dict(message.chat.id, "Task"), content_types=["text"])
def handle_task(message):
    global current_nandler
    global prev_part
    global prev_message
    global prev_type
    global not_advancing
    player = players[message.chat.id]
    if not not_advancing and player.current_part.check_advancing(message.text):
        prev_type = players[message.chat.id].part_type
        prev_part = players[message.chat.id].current_part
        prev_message = message
    else:
        not_advancing = True
    current_nandler.message = message
    new_player, transition = current_nandler.handle_task()
    players[message.chat.id] = new_player
    if transition == 2:
        current_nandler = Level_2.Level_2_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        prev_part = current_nandler.player.current_part
        prev_type = current_nandler.player.part_type
        prev_message = "Transition"
    elif transition == 3:
        current_nandler = Level_3.Level_3_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        prev_part = current_nandler.player.current_part
        prev_type = current_nandler.player.part_type
        prev_message.text = "Transition"
    elif transition == 4:
        current_nandler = Level_4.Level_4_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        prev_part = current_nandler.player.current_part
        prev_type = current_nandler.player.part_type
        prev_message.text = "Transition"
    elif transition == 5:
        current_nandler = Level_5.Level_5_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        prev_part = current_nandler.player.current_part
        prev_type = current_nandler.player.part_type
        prev_message.text = "Transition"
    elif transition == 6:
        current_nandler = Level_6.Level_6_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
        prev_part = current_nandler.player.current_part
        prev_type = current_nandler.player.part_type
        prev_message.text = "Transition"


# @server.route('/' + config.Token, methods=['POST'])
# def getMessage():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return "!", 200
#
# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='https://divinely-inspired-project.herokuapp.com/' + config.Token)
#     return "!", 200
#
# if __name__ == "__main__":
#     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8443)))

bot.polling(none_stop=True)
