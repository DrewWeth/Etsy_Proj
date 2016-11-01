from input_error import *
import sys
import manager
# start 18:20
# end 20:00
file_name = "sample_in.txt"
user_input_errors = []

def main():
    manager.Manager.instance = manager.Manager() # Sets up manager
    # read_input()
    main_thread()


def read_input():
    print("Welcome")
    with open(file_name) as f:
        for line in f:
            sipher_command(line.rstrip("\n"))

def educate_this_user():
    print("Yo, use the right commands")

def process_user_input(line):
    if line.lower() == "quit".lower():
        sys.exit(1)
    elif line.lower() == "help".lower():
        educate_this_user()
    else:
        sipher_command(line)

def sipher_command(line):
    raw_commands = line.split(" ")
    # print(raw_commands)
    if len(raw_commands) < 2:
        raise InputError('Command needs more commands. Type help for examples.')

    # TODO Make commands lower case standard.
    # Process main commands
    raw_commands[0] = raw_commands[0].lower()
    if sanitize_command(raw_commands, ['add', 'list', 'listen'], 0) == True:
        funcdict[raw_commands[0]](raw_commands)
    else:
        raise InputError("First command is invalid")

def sanitize_command(raw_commands, valid_commands, index):
    if raw_commands[index] in valid_commands:
        return True
    else:
        return False

def command_add(raw_commands):
    valid_commands = ['artist', 'album', 'track']
    if sanitize_command(raw_commands, valid_commands, 1) == False:
        raise InputError("Sub command (", raw_commands[1], ") is invalid. Use valid commands: ", valid_commands)
    subcommand_index = 2
    if raw_commands[1] == 'artist': # check to lower
        artist_name, count = get_artist_info(raw_commands, subcommand_index)
        manager.Manager.instance.add_artist(artist_name)
    elif raw_commands[1] == 'album':
        album_name, artist_name = get_album_info(raw_commands, subcommand_index)
        manager.Manager.instance.add_album(album_name, artist_name)
    elif raw_commands[1] == 'track':
        track_name, album_name, artist_name = get_track_info(raw_commands, subcommand_index)
        manager.Manager.instance.add_track(track_name, album_name, artist_name)
    else:
        print "ERR: command_add"

def get_artist_info(raw_commands, subcommand_index):
    artist_name, count = next_input(raw_commands, subcommand_index)
    return artist_name, count


# get_album_info takes an array of strings and a starting index and returns info for an album
# by sequentially searching for data
def get_album_info(raw_commands, subcommand_index):
    album_name, count = next_input(raw_commands, subcommand_index)
    by_index = subcommand_index + count
    # TODO Can check to make sure by_index has value "by"
    artist_name, count = next_input(raw_commands, by_index + 1)
    return [album_name, artist_name]

# get_track_info takes an array of strings and a starting index and returns info for a track
# by sequentially searching for data
def get_track_info(raw_commands, subcommand_index):
    track_name, count = next_input(raw_commands, subcommand_index)
    on_index = subcommand_index + count
    # TODO Can check to make sure by_index has value "by"
    album_name, count = next_input(raw_commands, on_index + 1)
    by_index = on_index + count + 1
    artist_name, count = next_input(raw_commands, by_index + 1)
    return [track_name, album_name, artist_name]

# next_input gets the next value from the raw_command data structure given a starting index.
# It returns an array of the value and number of elements joined to get value. [value, count]
# If the array at starting index begins with a quote, it finds the end quote and joins the values.
# If there's no quote, it returns the next value
def next_input(raw_commands, start_index):
    covers = 0
    if start_index >= len(raw_commands):
        raise InputError("Not enough information")
        return
    if raw_commands[start_index].startswith("\""): # Includes quotes
        for i in range(start_index, len(raw_commands)):
            covers += 1
            if raw_commands[i].endswith("\""):
                input_value = " ".join(raw_commands[start_index:i+1])[1:-1] # Extract quoted value and remove bookend quotes
                return [input_value, covers]
    else: # Did not include quotes
        return [raw_commands[start_index], 1]

def command_list(raw_commands):
    valid_commands = ['top', 'albums', 'tracks', 'artists']
    if sanitize_command(raw_commands, valid_commands, 1) == False:
        raise InputError("Sub command (", raw_commands[1], ") is invalid. Use valid commands: ", valid_commands)

    if raw_commands[1] == 'top':
        if not raw_commands[2].isdigit() and raw_commands[2] != 'q':
            raise InputError("Sub command (", raw_commands[2], ") is invalid. Use a number or letter 'q'")
        if raw_commands[2] == 'q':
            desired_count = -1
        else:
            desired_count = int(raw_commands[2])

        valid_commands = ['artists','tracks', 'albums']
        if sanitize_command(raw_commands, valid_commands, 3) == False:
            raise InputError("Sub command (", raw_commands[3], ") is invalid. Use valid commands: ", valid_commands)
        desired_category = raw_commands[3]

        if desired_category == 'artists':
            manager.Manager.instance.list_top_artists(desired_count)
        elif desired_category == 'tracks':
            manager.Manager.instance.list_top_tracks(desired_count)
        elif desired_category == 'albums':
            manager.Manager.instance.list_top_albums(desired_count)
        else:
            print "ERR: command_list top"
    else:
        valid_commands = ['albums', 'tracks', 'artists']
        if sanitize_command(raw_commands, valid_commands, 1) == False:
            raise InputError("Sub command (", raw_commands[1], ") is invalid. Use valid commands: ", valid_commands)
        desired_category = raw_commands[1]

        if desired_category == 'albums':
            result = get_album_info(raw_commands, 1)
            manager.Manager.instance.list_albums(result)
        elif desired_category == 'tracks':
            result = get_track_info(raw_commands, 1)
            manager.Manager.instance.list_tracks(result)
        elif desired_category == 'artists':
            manager.Manager.instance.list_artists()
        else:
            print "ERR: command_list normal", raw_commands


def command_listen(raw_commands):
    if len(raw_commands) < 4:
        raise InputError("Command usage: listen to 'song' on 'album' by 'artist'")
    track_values = get_track_info(raw_commands, 2)
    manager.Manager.instance.listen_to(track_values)


def main_thread():
    # user_input = 'add artist "a hello"'
    # user_input = 'add album album by artist'
    # user_input = 'add album "awesome album" by artist'
    # user_input = 'add track "track" on "awesome album" by artist'
    # user_input = "list top 3 tracks"
    # user_input='list tracks on "Not a real album" by "Smiling Lemurs"'

    automated = ['add artist bob',
    'add album foo by bob',
    'list albums by bob',
    'add track "sunday blues" on foo by bob',
    'add track "crushed heart" on foo by bob',
    'add track "rock on" on foo by bob',
    'list tracks on foo by bob',
    'listen to "sunday blues" on foo by bob',
    'list top 3 tracks',
    'add artist "Smiling Lemurs"',
    'add album "Sunbeams and Snowdrifts" by "Smiling Lemurs"',
    'list top 3 albums',
    'list top 3 artists']

    for user_input in automated:
        user_input = str(user_input.strip())
        process_user_input(user_input.rstrip("\n"))

    while True:
        try:
            # TODO: raw_input is < Python 3.0
            user_input = raw_input("Enter input:\n")

            user_input = str(user_input.strip())
            process_user_input(user_input.rstrip("\n"))
        except InputError as e:
            print "Input Error:", e.value
            sys.exc_clear()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

# Dictionary to functions
funcdict = {
  'add': command_add,
  'listen': command_listen,
  'list': command_list
}
main()
