
class Task:
    def __init__(self, raw_data, scenes, tasks):
        self.scenes = scenes
        self.tasks = tasks
        self.answers = raw_data["Answers"]
        self.text = raw_data["Text"]
        self.type = raw_data["Type"]
        self.task_number = raw_data["TaskNumber"]
        self.raw_data = raw_data

    def get_transition(self):
        if "Next_Level" in self.raw_data:
            return self.raw_data["Next_Level"]
        else:
            return 0

    def check_answer(self, message_text):
        return message_text in self.answers

    def get_response(self, message_text):
        return  self.answers[message_text]["Response"]

    def get_photo_id(self):
        if "PhotoId" in self.raw_data:
            return self.raw_data["PhotoId"]
        return ""

    def check_advancing(self, message_text):
        return self.type != self.answers[message_text]["Type"] or \
               self.task_number != self.answers[message_text]["Goto"]

    def get_next(self, message):
        change = self.check_advancing(message)
        type = self.answers[message]["Type"]
        if type == "Task":
            return (Task(self.tasks[self.answers[message]["Goto"]], self.scenes, self.tasks), change)
        from Scene import Scene
        return (Scene(self.scenes[self.answers[message]["Goto"]], self.scenes, self.tasks), change)

    def level_1_check_task_correctness(self, answer):
        if self.task_number > 0:
            return self.answers[answer]["Correct"] == "True"
        return False

