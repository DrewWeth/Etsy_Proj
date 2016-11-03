from input_error import InputError
# This file contains functions that help extract data from either raw strings or the raw_command data structure

# sanitize_command: Returns true iff the a valid command exists at the index of raw_commands in all lowercase
def sanitize_command(raw_commands, valid_commands, index):
    if index >= len(raw_commands):
        return False
    raw_commands[index] = raw_commands[index].lower() # Forces downcase
    if raw_commands[index] in valid_commands:
        return True
    else:
        return False

# get_artist_info: Given the raw_commands data structure, and the start of artist
# data, it extracts artist name and how many elements were joined to get the artist name.
def get_artist_info(raw_commands, subcommand_index):
    artist_name, count = next_input(raw_commands, subcommand_index)
    if count < 0:
        raise InputError("Need more info. Please include artist name")
    return artist_name, count

# get_album_info: Takes an array of strings and a starting index and returns
# the album name and artist name or raises an error.
def get_album_info(raw_commands, subcommand_index):
    album_name, count = next_input(raw_commands, subcommand_index)
    if count < 0:
        raise InputError("Need more info. Please include album name")
    by_index = subcommand_index + count
    artist_name, count = next_input(raw_commands, by_index + 1)
    if count < 0:
        raise InputError("Need more info. Please include 'by' and the 'artists name' after the album name")
    return [album_name, artist_name]

# get_track_info: Takes an array of strings and a starting index and returns
# tack name, album_name, and artist_name
def get_track_info(raw_commands, subcommand_index):
    track_name, count = next_input(raw_commands, subcommand_index)
    if count < 0:
        raise InputError("Need more info. Please include track name")
    on_index = subcommand_index + count
    album_name, count = next_input(raw_commands, on_index + 1)
    if count < 0:
        raise InputError("Need more info. Please include 'on' and 'album name' after the track name")
    by_index = on_index + count + 1
    artist_name, count = next_input(raw_commands, by_index + 1)
    if count < 0:
        raise InputError("Need more info. Please include 'by' and 'artist name' after the album name")
    return [track_name, album_name, artist_name]

# next_input: Gets the next value from the raw_command data structure given a starting index.
# It returns an array of the next value and number of elements joined to get value. [value, count]
# If the array at starting index begins with a quote, it finds the end quote and joins the values.
# If there's no quote, it returns the next value
def next_input(raw_commands, start_index):
    covers = 0
    if start_index >= len(raw_commands):
        return ["", -1]
    if raw_commands[start_index].startswith("\""): # includes double quotes
        for i in range(start_index, len(raw_commands)):
            covers += 1
            if raw_commands[i].endswith("\""):
                input_value = " ".join(raw_commands[start_index:i+1])[1:-1] # Extract quoted value and remove bookend quotes
                return [input_value, covers]
    else: # does not include double quotes
        return [raw_commands[start_index], 1]
    return ["", -1]
