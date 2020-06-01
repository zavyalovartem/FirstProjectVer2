import JsonScenes
import os
import json
import Theory
from telebot import types
import Player

class Theory_Handler:
    def __init__(self, bot, message):
        global theory
        path = os.getcwd() + "/JsonScenes"
        with open(path + "/Theory.json", encoding="utf-8") as f:
            theory = json.loads(f.read())
        self.player = Player.Player(0, 0, Theory.Theory(theory[0], theory, message), "Theory")
        self.message = message
        self.bot = bot

    def handle_start(self):
        markup = self.generate_markup_for_theory(self.player.current_part.answers)
        self.bot.send_message(self.message.chat.id, self.player.current_part.text, reply_markup= markup)

    def handle_theory(self):
        current_part = self.player.current_part
        if not current_part.check_answer(self.message.text):
            self.bot.send_message(self.message.chat.id, "Incorrect answer")
        else:
            response = current_part.get_response(self.message.text)
            if response != "":
                self.bot.send_message(self.message.chat.id, response)
            next_part = self.player.current_part.get_next(self.message)
            markup = self.generate_markup_for_theory(self.player.current_part.answers)
            if self.player.current_part.get_photo_id(self.message) != "":
                id = self.player.current_part.get_photo_id(self.message)
                self.bot.send_photo(self.message.chat.id, id)
            self.player.current_part = next_part
            self.bot.send_message(self.message.chat.id, self.player.current_part.text, reply_markup=markup)
        return self.player


    def generate_markup_for_theory(self, answers):
        markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
        for answer in answers:
            markup.add(answer)
        markup.add("Вернуться к игре")
        return markup