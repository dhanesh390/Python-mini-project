class DataNotFoundException(Exception):
    def __init__(self, message=None, *args):
        if message:
            self.message = message
        print("Created")

    def __str__(self):
        print("TESTTTTTTTTTTTTTTTTTTTTTt")
        if self.message:
            return self.message
        else:
            return 'No data found'


class InvalidInput(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'{self.message}'
        else:
            return 'Invalid input, Enter again'


class InvalidValue(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'{self.message}'
        else:
            return 'Invalid value, Enter again'
