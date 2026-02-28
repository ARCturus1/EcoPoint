class MissingException(Exception):
    def __init__(self, message):
        self.message = message


class DuplicateException(Exception):
    def __init__(self, message):
        self.message = message
