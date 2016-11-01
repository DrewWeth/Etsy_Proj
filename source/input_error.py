class InputError(Exception):
    def __init__(self, *args):
        self.value = ' '.join(map(str, args))
    def __str__(self):
        return repr(self.value)
