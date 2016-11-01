from __future__ import print_function # Backwards Compatibility: Ensures that built in print function from <3.0 Python prints string instead of tuple.
from input_error import *
from manager import *
from extractor import *
import sys

file_name = "sample_in.txt"

def main():
    Manager.instance = Manager() # Sets up manager
    # read_input()
    main_thread()

def educate_this_user():
    print("There are 3 main commands: add, list, and listen.")
    print(hilite("----ADD COMMAND----", 1, True))
    print("The add command has 3 sub commands: artist, album, and track.")
    print("Before adding an album, the artist must exist.")
    print("Before adding a track, the album and artist must exist.")
    print("USAGE: add artist bob")
    print('USAGE: add album "The amazing race" by bob')
    print('USAGE: add track "The amazing race"')
    print(hilite("----LIST COMMAND----", 1, True))
    print("The list command has 3 subcommands and 1 optional value: artists, albums, tracks, and [top].")
    print("USAGE: list artists")
    print("USAGE: list albums by bob")
    print("USAGE: list tracks on \"Album Name\" by bob")
    print("USAGE: list top q albums")
    print("USAGE: list top 3 tracks")
    print(hilite("----LISTEN COMMAND----", 1, True))
    print("This command increments the play count on a track. You must provide the track, album, and artist.")
    print("USAGE: listen to \"song\" on \"album name\" by bob")
    print(hilite("----END----", True, True))

def process_user_input(line):
    if line.lower() == "quit".lower():
        sys.exit(1)
    elif line.lower() == "help".lower():
        educate_this_user()
    else:
        sipher_command(line)

def read_input():
    with open(file_name) as f:
        for line in f:
            sipher_command(line.rstrip("\n"))

def sipher_command(line):
    raw_commands = line.split(" ") # Main data structure used to interpret user data.
    if len(raw_commands) < 1:
        raise InputError('Command needs more commands. Type help for examples.')

    # Process main commands
    primary_commands = ['add', 'list', 'listen']
    if sanitize_command(raw_commands, primary_commands, 0) == True:
        funcdict[raw_commands[0]](raw_commands)
    else:
        raise InputError("First command is invalid. Use one of these", primary_commands)

# command_add handles all logic of the 'add' command and subcommands after the we've determined the user wants to add something
def command_add(raw_commands):
    valid_commands = ['artist', 'album', 'track']
    if sanitize_command(raw_commands, valid_commands, 1) == False:
        raise InputError("Sub command is invalid. Use valid commands: ", valid_commands, "after add")
        return
    subcommand_index = 2
    if raw_commands[1] == 'artist': # check to lower
        artist_name, count = get_artist_info(raw_commands, subcommand_index)
        Manager.instance.add_artist(artist_name)
    elif raw_commands[1] == 'album':
        album_name, artist_name = get_album_info(raw_commands, subcommand_index)
        Manager.instance.add_album(album_name, artist_name)
    elif raw_commands[1] == 'track':
        track_name, album_name, artist_name = get_track_info(raw_commands, subcommand_index)
        Manager.instance.add_track(track_name, album_name, artist_name)
    else:
        print("ERR: command_add")

# command_list handles all logic to display lists and handling subcommands after we've determine the user wants to list something
def command_list(raw_commands):
    valid_commands = ['top', 'albums', 'tracks', 'artists']
    if sanitize_command(raw_commands, valid_commands, 1) == False:
        raise InputError("Sub command is invalid. Use valid commands: ", valid_commands, "after list")

    if raw_commands[1] == 'top':
        value, count = next_input(raw_commands, 2)
        if count < 0:
            raise InputError("Please enter how many to print. To print all value input 'q'")
        if not value.isdigit() and value != 'q':
            raise InputError("Sub command is invalid. Use a number or letter 'q'")
        if value == 'q':
            desired_count = -1
        else:
            desired_count = int(value)

        valid_commands = ['artists','tracks', 'albums']
        if sanitize_command(raw_commands, valid_commands, 3) == False:
            raise InputError("Sub command is invalid. Use valid commands: ", valid_commands)
        desired_category = raw_commands[3]

        if desired_category == 'artists':
            Manager.instance.list_top_artists(desired_count)
        elif desired_category == 'tracks':
            Manager.instance.list_top_tracks(desired_count)
        elif desired_category == 'albums':
            Manager.instance.list_top_albums(desired_count)
        else:
            print("ERR: command_list top")
    else:
        valid_commands = ['albums', 'tracks', 'artists']
        if sanitize_command(raw_commands, valid_commands, 1) == False:
            raise InputError("Sub command (", raw_commands[1], ") is invalid. Use valid commands: ", valid_commands)
        desired_category = raw_commands[1]
        if desired_category == 'albums':
            result = get_album_info(raw_commands, 1)
            Manager.instance.list_albums(result)
        elif desired_category == 'tracks':
            result = get_track_info(raw_commands, 1)
            Manager.instance.list_tracks(result)
        elif desired_category == 'artists':
            Manager.instance.list_artists()
        else:
            print("ERR: command_list normal", raw_commands)

# command_listen handles logic to find a desired track and increment it's play_count
def command_listen(raw_commands):
    if len(raw_commands) < 4:
        raise InputError("Command usage: listen to \"song\" on \"album\" by \"artist\"")
    track_values = get_track_info(raw_commands, 2)
    Manager.instance.listen_to(track_values)

# Abstraction for string emphasis. Useful in a bland CLI
def hilite(string, status, bold):
    attr = []
    if status == 1:
        attr.append('32') # green
    elif status == -1:
        attr.append('31') # Red
    if bold:
        attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

def run_test():
    # automated = ['add artist bob',
    # 'add album foo by bob',
    # 'list albums by bob',
    # 'add track "sunday blues" on foo by bob',
    # 'add track "crushed heart" on foo by bob',
    # 'add track "rock on" on foo by bob',
    # 'list tracks on foo by bob',
    # 'listen to "sunday blues" on foo by bob',
    # 'list top 3 tracks',
    # 'add artist "Smiling Lemurs"',
    # 'add album "Sunbeams and Snowdrifts" by "Smiling Lemurs"',
    # 'list top 3 albums',
    # 'list top 3 artists']
    # for user_input in automated:
    #     user_input = str(user_input.strip())
    #     process_user_input(user_input.rstrip("\n"))

def main_thread():
    run_test()
    print("Welcome to Music Manager. Type help to get started or", hilite("quit", 1, True) ,"to quit, or", hilite("help", 1, True), "for help.")
    while True:
        try:
            # raw_input was renamed to input in Python3.0, this allows support for 2.7 which is widely and 2.6 which is stock on Mac machines.
            try: user_input = raw_input("")
            except NameError:
                pass
                user_input = input("")

            user_input = str(user_input.rstrip("\n").strip().decode('utf-8')) # Strip newline, strip outter tabs and spaces, ensure utf-8
            process_user_input(user_input)
        except InputError as e:
            print(hilite("Input Error:", -1, True), e.value)
            sys.exc_clear()
        except:
            sys.exit(1)
            # print("Unexpected error:", sys.exc_info()[0])
            # raise

# Dictionary to functions
funcdict = {
  'add': command_add,
  'listen': command_listen,
  'list': command_list
}

main() # Initial point of execution. Runs the program.
