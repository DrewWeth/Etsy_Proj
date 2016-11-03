from __future__ import print_function
from input_error import InputError
import artist, album, track
# from bisect import bisect_left
from operator import itemgetter, attrgetter, methodcaller

class MusicDatastore:
    instance = None # Maintains one instance of MusicDatastore as static variable

    def __init__(self):
        self.artists = {} # Artists are mainly looked up, not listed
        self.albums = []
        self.tracks = []

    def add_artist(self,name):
        new_artist = artist.Artist(name)
        self.artists[name] = new_artist
        return new_artist

    def add_album(self, album_name, artist_name):
        if artist_name not in self.artists:
            raise InputError('Artist not found. Please add artist')
        artist = self.artists[artist_name] # Find instance of artist
        new_album = album.Album(album_name)
        self.albums.append(new_album)
        new_album.artist = artist # Album to artist connection
        artist.albums[album_name] = new_album # Artist to album connection
        return new_album

    def add_track(self, track_name, album_name, artist_name):
        if artist_name not in self.artists:
            raise InputError('Artist not found. Please add artist')
        artist = self.artists[artist_name]
        new_track = track.Track(track_name, album_name, artist_name)
        self.tracks.append(new_track)
        if album_name not in artist.albums:
            raise InputError('Album not found. Please add album.')
        album = artist.albums[album_name]
        album.tracks[track_name] = new_track # Connection from album to track
        new_track.album = album # Connection from track to album
        new_track.artist = artist # Connection from track to artist. Maybe unecessary
        return new_track

    # Sorts tracks by play count and prints 'count' number of results. Prints all results if 'count' < 0
    def list_top_tracks(self, count):
        sorted_tracks = sorted(self.tracks, key=attrgetter('play_count'), reverse=True)
        desired_range = appropriate_range(sorted_tracks, count)
        for i, track in enumerate(desired_range):
            print(i+1, "Track plays:", track.play_count, "- \"", track.name, "\"", "by", track.album.artist.name)
        return desired_range

    def aggregate_album_plays(self, album):
        plays = 0
        for key in album.tracks:
            plays += album.tracks[key].play_count
        return [album, plays]

    def list_top_artists(self, count):
        unsorted_artists = [self.aggregate_artist_plays(self.artists[artist_key]) for artist_key in self.artists]
        unsorted_artists = sorted(unsorted_artists, key=lambda x: x[1], reverse=True)
        desired_range = appropriate_range(unsorted_artists, count)
        for idx,artist_data in enumerate(desired_range):
            print(idx+1, "Artist plays:", artist_data[1], "-", artist_data[0].name)
        return desired_range

    def aggregate_artist_plays(self, artist):
        plays = 0
        for album_name in artist.albums:
            plays += self.aggregate_album_plays(artist.albums[album_name])[1]
        return [artist, plays]

    def list_top_albums(self, count):
        unsorted_albums = [self.aggregate_album_plays(album) for album in self.albums]
        unsorted_albums.sort(key=lambda x: x[1], reverse=True)
        desired_range = appropriate_range(unsorted_albums, count)
        for idx,album_data in enumerate(desired_range):
            print(idx+1, "Album plays:", album_data[1], "-", album_data[0].name)
        return desired_range

    def list_tracks(self, track_values):
        if track_values[2] not in self.artists:
            raise InputError('Artist not found. Please add artist')
        artist = self.artists[track_values[2]] # Find instance of artist
        if track_values[1] not in artist.albums:
            raise InputError("Album does not exist")
        album = artist.albums[track_values[1]]
        for idx,track in enumerate(album.tracks):
            print(idx+1, track)

    def list_artists(self):
        # print "Listing artists"
        for idx, artist_name in enumerate(self.artists):
            print(idx+1, self.artists[artist_name].name)

    def list_albums(self, album_values):
        if album_values[1] not in self.artists:
            raise InputError('Artist not found. Please add artist')
        artist = self.artists[album_values[1]] # Find instance of artist
        for idx, album in enumerate(artist.albums):
            print(idx+1, album)

    def locate_track(self, track_values):
        if track_values[2] not in self.artists:
            raise InputError('Artist not found. Check spelling or add artist')
        artist = self.artists[track_values[2]] # Find instance of artist
        if track_values[1] not in artist.albums:
            raise InputError("Album does not exist. Check spelling.")
        album = artist.albums[track_values[1]]
        if track_values[0] not in album.tracks:
            raise InputError("Track does not exist. Check spelling.")
        return album.tracks[track_values[0]]

    def listen_to(self, track_values):
        track = self.locate_track(track_values)
        track.play_count += 1

    # Look up table from string to function to avoid switch/if statements. Implements tell dont ask
    funcdict = {
        'add_artist': add_artist,
        'add_track':add_track,
        'add_album':add_album
    }

    def clear():
        self.artists = {}
        self.albums = []
        self.tracks = []

# appropriate_range returns either the top few results or all of the results
# It abstracts away doing conditional slicing
def appropriate_range(whole_arr, count):
    if count < 0:
        appropriate_range = whole_arr[:]
    else:
        appropriate_range = whole_arr[:count]
    return appropriate_range

# Returns singleton in the form of static value a manaager instance
def get_music_datastore():
    if MusicDatastore.instance != None:
        return MusicDatastore.instance
    else:
        MusicDatastore.instance = MusicDatastore() # Sets up MusicDatastore
        return MusicDatastore.instance
