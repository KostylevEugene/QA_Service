class EntityAlreadyExistError(Exception):
    def __init__(self, msg):
        self.msg = msg
