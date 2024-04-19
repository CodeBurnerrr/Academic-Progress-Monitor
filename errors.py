
class InvalidMarksError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidInputError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
class EnrollmentError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class EmailError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class PasswordError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)



