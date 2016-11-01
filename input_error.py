class InputError(Exception):
    def __init__(self, *args):
        self.value = ""
        # TODO: Rewrite joining tuple into string
        for val in args:
            self.value += str(val)
    def __str__(self):
        return repr(self.value)
