from input_error import *
import artist, album, track
# from bisect import bisect_left
from operator import itemgetter, attrgetter, methodcaller

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
        artist = self.binary_search(self.artists, artist_name) # Find instance of artist
        if artist == None:
            raise InputError('Artist not found. Please add artist')
        new_album = album.Album(album_name)
        # print "New album:", new_album.name
        self.albums.append(new_album)
        self.albums.sort(key=lambda x: x.name)
        new_album.artist = artist # Album to artist connection
        artist.albums[album_name] = new_album # Artist to album connection

    def add_track(self, track_name, album_name, artist_name):
        new_track = track.Track(track_name, album_name, artist_name)
        self.tracks.append(new_track)
        self.tracks.sort(key=lambda x: x.name)
        artist = self.binary_search(self.artists, artist_name) # Find instance of artist
        album = artist.albums[album_name]
        album.tracks[track_name] = new_track
        new_track.album = album


    # Sorts tracks by play count and prints 'count' number of results. Prints all results if 'count' < 0
    def list_top_tracks(self, count):
        sorted_tracks = sorted(self.tracks, key=attrgetter('play_count'), reverse=True)
        if count < 0:
            desired_range=sorted_tracks[:]
        else:
            desired_range=sorted_tracks[:count]
        for i, track in enumerate(desired_range):
            print i+1, "Track plays:", track.play_count, track.name

    def aggregate_album_plays(self, album):
        plays = 0
        for key in album.tracks:
            plays += album.tracks[key].play_count
        return [album, plays]

    def list_top_artists(self, count):
        unsorted_artists = [self.aggregate_artist_plays(artist) for artist in self.artists]
        unsorted_artists.sort(key=lambda x: x[1], reverse=True)
        for idx,artist_data in enumerate(unsorted_artists):
            print idx+1, "Artist Plays", artist_data[1], artist_data[0].name

    def aggregate_artist_plays(self, artist):
        plays = 0
        for album_name in artist.albums:
            plays += self.aggregate_album_plays(artist.albums[album_name])[1]
        return [artist, plays]

    def list_top_albums(self, count):
        unsorted_albums = [self.aggregate_album_plays(album) for album in self.albums]
        unsorted_albums.sort(key=lambda x: x[1], reverse=True)
        for idx,album_data in enumerate(unsorted_albums):
            print idx+1, "Album Plays", album_data[1], album_data[0].name

    def list_tracks(self, track_values):
        print track_values
        # print "Listing tracks for", track_values[1], "by", track_values[2]
        artist = self.binary_search(self.artists, track_values[2])
        if artist == None:
            raise InputError("Artist does not exist")
        if track_values[1] not in artist.albums:
            raise InputError("Album does not exist")
        album = artist.albums[track_values[1]]
        for idx,track in enumerate(album.tracks):
            print idx+1, track

    def list_artists(self):
        # print "Listing artists"
        for idx, artist in enumerate(self.artists):
            print idx+1, artist.name

    def list_albums(self, album_values):
        # print "List albums for",album_values[1]
        artist = self.binary_search(self.artists, album_values[1])
        if artist == None:
            raise InputError("Artist does not exist")
        for idx, album in enumerate(artist.albums):
            print idx+1, album


    def locate_track(self, track_values):
        artist = self.binary_search(self.artists, track_values[2])
        if artist == None:
            raise InputError("Artist does not exist. Check spelling.")
        if track_values[1] not in artist.albums:
            raise InputError("Album does not exist. Check spelling.")
        album = artist.albums[track_values[1]]
        if track_values[0] not in album.tracks:
            raise InputError("Track does not exist. Check spelling.")
        return album.tracks[track_values[0]]

    def listen_to(self, track_values):
        track = self.locate_track(track_values)
        print 'track value:', track
        track.play_count += 1

    # Look up table from string to function to avoid switch/if statements. Implements tell dont ask
    funcdict = {
    'add_artist': add_artist,
    'add_track':add_track,
    'add_album':add_album
    }

    # Returns singleton in the form of static value a manaager instance
    def manager():
        return instance
