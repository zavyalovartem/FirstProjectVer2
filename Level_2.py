import JsonScenes
import os
import json
import Scene
import Task
from telebot import types

scenes = {}
tasks = {}

class Level_2_Handler:
    def __init__(self, player_id, message, bot):
        global scenes
        global tasks
        path = os.getcwd() + "/JsonScenes"
        with open(path + "/Tasks_Level_2.json", encoding="utf-8") as f:
            tasks = json.loads(f.read())
        with open(path + "/Scenes_Level_2.json", encoding="utf-8") as f:
            scenes = json.loads(f.read())
        from Player import Player
        self.player = Player(0, 0, Task.Task(tasks[0], scenes, tasks), "Task")
        self.message = message
        self.bot = bot

    def handle_start(self):
        markup = self.generate_markup(self.player.current_part.answers)
        self.bot.send_photo(self.message.chat.id, "AgACAgIAAxkDAAIFyV7NAsVA14AQnLS_qKkvTzrxK3GGAAJirjEb0adoSmG5uT6SWDsmwh5Nky4AAwEAAwIAA3kAAz4MAAIZBA")
        if self.player.current_part.get_photo_id() != "":
            self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(), self.player.current_part.text,
                            reply_markup= markup)
        else:
            self.bot.send_message(self.message.chat.id, self.player.current_part.text, reply_markup= markup)

    def handle_scene(self):
        current_part = self.player.current_part
        transition = 0
        if not current_part.check_answer(self.message.text):
            self.bot.send_message(self.message.chat.id, "Incorrect answer")
        else:
            response = current_part.get_response(self.message.text)
            if response != "":
                self.bot.send_message(self.message.chat.id, response)
            next_part, flag = current_part.get_next(self.message.text)
            if flag:
                self.player.current_part = next_part
                markup = self.generate_markup(self.player.current_part.answers)
                if self.player.current_part.get_photo_id() != "":
                    self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(), self.player.current_part.text,
                                   reply_markup=markup)
                else:
                    self.bot.send_message(self.message.chat.id, self.player.current_part.text, reply_markup=markup)
                transition = self.player.current_part.get_transition()
                self.player.part_type = next_part.type
        return (self.player, transition)

    def handle_task(self):
        current_part = self.player.current_part
        transition = 0
        if not current_part.check_answer(self.message.text):
            self.bot.send_message(self.message.chat.id, "Incorrect answer")
        else:
            response = current_part.get_response(self.message.text)
            if response != "":
                self.bot.send_message(self.message.chat.id, response)
            next_part, flag = current_part.get_next(self.message.text)
            if flag:
                self.player.current_part = next_part
                markup = self.generate_markup(self.player.current_part.answers)
                if self.player.current_part.get_photo_id() != "":
                    self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(), self.player.current_part.text,
                                   reply_markup= markup)
                else:
                    self.bot.send_message(self.message.chat.id, self.player.current_part.text, reply_markup=markup)
                transition = self.player.current_part.get_transition()
                self.player.part_type = next_part.type
        return (self.player, transition)



    def generate_markup(self, answers):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for answer in answers:
            markup.add(answer)
        markup.add("Теория")
        return markup