import JsonScenes
import os
import json
import Scene
import Task
from telebot import types

scenes = {}
tasks = {}

class Level_5_Handler:
    def __init__(self, player_id, message, bot):
        global scenes
        global tasks
        path = os.getcwd() + "/JsonScenes"
        with open(path + "/Tasks_Level_5.json", encoding="utf-8") as f:
            tasks = json.loads(f.read())
        with open(path + "/Scenes_Level_5.json", encoding="utf-8") as f:
            scenes = json.loads(f.read())
        from Player import Player
        self.player = Player(0, 0, Scene.Scene(scenes[0], scenes, tasks), "Scene")
        self.message = message
        self.bot = bot
        self.first_part_correct = 0

    def handle_start(self):
        markup = self.generate_markup(self.player.current_part.answers)
        self.bot.send_photo(self.message.chat.id, "AgACAgIAAxkDAAIFz17NAuOXIRlHKVx4xaJRBvvNRnQEAAJlrjEb0adoSuoEdUxoojWXZym8ki4AAwEAAwIAA3kAAyd2AgABGQQ")
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
                if next_part.type == "Task":
                    if self.player.current_part.get_photo_id() != "":
                        self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(),
                                            self.player.current_part.text, reply_markup= types.ReplyKeyboardRemove())
                    else:
                        self.bot.send_message(self.message.chat.id, self.player.current_part.text,
                                              reply_markup= types.ReplyKeyboardRemove())
                else:
                    if self.player.current_part.get_photo_id() != "":
                        self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(), self.player.current_part.text,
                                            reply_markup= markup)
                    else:
                        self.bot.send_message(self.message.chat.id, self.player.current_part.text, reply_markup= markup)
                transition = self.player.current_part.get_transition()
                self.player.part_type = next_part.type
        return (self.player, transition)

    def handle_task(self):
        current_part = self.player.current_part
        transition = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Теория")
        if not current_part.check_answer(self.message.text):
            next_part = current_part.level_5_get_next_for_incorrect()
            self.player.current_part = next_part
            if self.player.current_part.type == "Scene" and self.player.current_part.scene_number == 13:
                if self.first_part_correct > 3:
                    next_part = self.player.current_part.level_5_return_first_part_success()
                    self.player.current_part = next_part
                    markup = self.generate_markup(self.player.current_part.answers)
                    if self.player.current_part.get_photo_id() != "":
                        self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(),
                                            self.player.current_part.text, reply_markup=markup)
                    else:
                        self.bot.send_message(self.message.chat.id, self.player.current_part.text, reply_markup=markup)
                    self.player.part_type = next_part.type
                    return (self.player, 0)
                else:
                    next_part = self.player.current_part.level_5_return_if_first_part_fail()
                    self.player.current_part = next_part
                    markup = self.generate_markup(self.player.current_part.answers)
                    if self.player.current_part.get_photo_id() != "":
                        self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(),
                                            self.player.current_part.text, reply_markup=markup)
                    else:
                        self.bot.send_message(self.message.chat.id, self.player.current_part.text, reply_markup=markup)
                    self.player.part_type = next_part.type
                    return (self.player, 0)
            if self.player.current_part.type != "Scene":
                if self.player.current_part.get_photo_id() != "":
                    self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(),
                                        self.player.current_part.text)
                else:
                    self.bot.send_message(self.message.chat.id, self.player.current_part.text)
            else:
                if self.player.current_part.scene_number < 6:
                    self.bot.send_message(self.message.chat.id, "Incorrect answer")
                else:
                    markup = self.generate_markup(self.player.current_part.answers)
                    if self.player.current_part.get_photo_id() != "":
                        self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(),
                                            self.player.current_part.text, reply_markup=markup)
                    else:
                        self.bot.send_message(self.message.chat.id, self.player.current_part.text, reply_markup=markup)
            transition = self.player.current_part.get_transition()
            self.player.part_type = next_part.type
        else:
            self.first_part_correct += 1
            response = current_part.get_response(self.message.text)
            if response != "":
                self.bot.send_message(self.message.chat.id, response)
            next_part, flag = current_part.get_next(self.message.text)
            if flag:
                self.player.current_part = next_part
                if self.player.current_part.type == "Scene" and self.player.current_part.scene_number == 13:
                    if self.first_part_correct > 3:
                        next_part = self.player.current_part.level_5_return_first_part_success()
                        self.player.current_part = next_part
                        markup = self.generate_markup(self.player.current_part.answers)
                        if self.player.current_part.get_photo_id() != "":
                            self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(),
                                                self.player.current_part.text, reply_markup= markup)
                        else:
                            self.bot.send_message(self.message.chat.id, self.player.current_part.text, reply_markup= markup)
                        self.player.part_type = next_part.type
                        return (self.player, 0)
                    else:
                        next_part = self.player.current_part.level_5_return_if_first_part_fail()
                        self.player.current_part = next_part
                        markup = self.generate_markup(self.player.current_part.answers)
                        if self.player.current_part.get_photo_id() != "":
                            self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(),
                                                self.player.current_part.text, reply_markup= markup)
                        else:
                            self.bot.send_message(self.message.chat.id, self.player.current_part.text, reply_markup= markup)
                        self.player.part_type = next_part.type
                        return (self.player, 0)
                if self.player.current_part.type != "Scene":
                    if self.player.current_part.get_photo_id() != "":
                        self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(), self.player.current_part.text)
                    else:
                        self.bot.send_message(self.message.chat.id, self.player.current_part.text)
                else:
                    markup = self.generate_markup(self.player.current_part.answers)
                    if self.player.current_part.get_photo_id() != "":
                        self.bot.send_photo(self.message.chat.id, self.player.current_part.get_photo_id(), self.player.current_part.text, reply_markup= markup)
                    else:
                        self.bot.send_message(self.message.chat.id, self.player.current_part.text, reply_markup= markup)
                transition = self.player.current_part.get_transition()
                self.player.part_type = next_part.type
        return (self.player, transition)



    def generate_markup(self, answers):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for answer in answers:
            markup.add(answer)
        markup.add("Теория")
        return markup