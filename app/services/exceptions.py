class QuestionAlreadyExists(Exception):
    def __init__(self, msg):
        self.msg = msg

class QuestionNotExists(Exception):
    def __init__(self, msg):
        self.msg = msg

class AnswerNotExists(Exception):
    def __init__(self, msg):
        self.msg = msg
