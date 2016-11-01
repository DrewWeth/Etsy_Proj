import artist, album, track
from bisect import bisect_left

class Manager:
    instance = None # Maintains one instance of Manager as static variable

    def __init__(self):
        self.artists = []
        self.albums = []
        self.tracks = []
        # self.instance = self
        # print self.instance

    def binary_search(self, L, target):
        start = 0
        end = len(L) - 1

        while start <= end:
            middle = (start + end)/ 2
            midpoint = L[middle]
            if midpoint.name > target:
                end = middle - 1
            elif midpoint.name < target:
                start = middle + 1
            else:
                return midpoint
        return None

    def add_artist(self,name):
        new_artist = artist.Artist(name)
        self.artists.append(new_artist)
        self.artists.sort(key=lambda x: x.name)

    def add_album(self, album_name, artist_name):
        new_album = album.Album(album_name)
        self.albums.append(new_album)
        self.albums.sort(key=lambda x: x.name)
        artist = self.binary_search(self.artists, artist_name) # Find instance of artist
        new_album.artist = artist # Album to artist connection
        artist.albums[album_name] = new_album # Artist to album connection

    def add_track(self, track_name, album_name, artist_name):
        new_track = track.Track(track_name, album_name, artist_name)
        self.artists.append(new_track)
        self.tracks.sort(key=lambda x: x.name)
        artist = self.binary_search(self.artists, artist_name) # Find instance of artist
        album = artist.albums[album_name]
        album.tracks[track_name] = new_track
        new_track.album = album


    def list_top_artists(self, count):
        return

    def list_top_tracks(self, count):
        for track in self.tracks:
            # print track
            return


    funcdict = {
    'add_artist': add_artist,
    'add_track':add_track,
    'add_album':add_album
    }

    def manager():
        return instance
