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
import time

bot = telebot.TeleBot(config.Token)
global players
global Started
Started = False
players = {}
global current_nandler

@bot.message_handler(commands=['test'])
def get_ids(message):
    bot.send_message(message.chat.id, "Intros")
    path = os.getcwd() + "/Illustrations/Intros"
    for file in os.listdir(path):
        f = open(path + '/' + file, 'rb')
        msg = bot.send_photo(message.chat.id, f)
        bot.send_message(message.chat.id, msg.photo[2].file_id, reply_to_message_id=msg.message_id)
    time.sleep(3)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global Started
    global players
    global current_nandler
    text_directory = os.getcwd() + "/JsonScenes"
    if Started == False:
        Started = True
        current_nandler = Level_1.Level_1_Handler(message.chat.id, message, bot)
        players[message.chat.id] = current_nandler.player
        current_nandler.handle_start()
    else:
        bot.send_message(message.chat.id, "Твоё приключение уже началось")

def check_player_in_dict(id, type):
    if id not in players:
        return False
    return id in players and players[id].part_type == type

@bot.message_handler(func=lambda message: check_player_in_dict(message.chat.id, "Scene"), content_types=['text'])
def handle_scene(message):
    global current_nandler
    player = players[message.chat.id]
    current_nandler.message = message
    new_player, transition = current_nandler.handle_scene()
    players[message.chat.id] = new_player
    if transition == 2:
        current_nandler = Level_2.Level_2_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
    elif transition == 3:
        current_nandler = 3

@bot.message_handler(func=lambda message: check_player_in_dict(message.chat.id, "Task"), content_types=["text"])
def handle_task(message):
    global current_nandler
    player = players[message.chat.id]
    current_nandler.message = message
    new_player, transition = current_nandler.handle_task()
    players[message.chat.id] = new_player
    if transition == 2:
        current_nandler = Level_2.Level_2_Handler(message.chat.id, message, bot)
        current_nandler.handle_start()
    elif transition == 3:
        current_nandler = 3



bot.infinity_polling()