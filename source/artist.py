class Artist:
    def __init__(self, name):
        self.name = name
        self.albums = {} # Map is used instead of an array because albums are commonly looked up instead of listed
