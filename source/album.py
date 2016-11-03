class Album:
    def __init__(self, name):
        self.name = name
        self.artist = None
        self.tracks = {} # Map is used instead of an array because tracks are commonly looked up instead of listed
