class Theory:
    def __init__(self, raw_data, theory, message):
        self.raw_data = raw_data
        self.answers = raw_data["Answers"]
        self.number = raw_data["SceneNumber"]
        self.theory = theory
        self.text= raw_data["Text"]
        self.message = message

    def check_answer(self, message_text):
        return message_text in self.answers

    def get_response(self, message_text):
        return  self.answers[message_text]["Response"]

    def get_photo_id(self, message):
        if "PhotoId" in self.answers[message.text]:
            test = self.answers[message.text]
            return self.answers[message.text]["PhotoId"]
        return ""

    def check_advancing(self, message_text):
        return self.type != self.answers[message_text]["Type"] or \
               self.task_number != self.answers[message_text]["Goto"]

    def get_next(self, message):
        return Theory(self.theory[self.answers[message.text]["Goto"]], self.theory, message)