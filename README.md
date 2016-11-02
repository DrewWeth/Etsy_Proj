# Etsy_Proj
This project is a homework problem that implements a music manager command line interface. It features interfaces to add artists, albums, and tracks. It can 'listen' to tracks and list top listened-to artists, albums, and tracks.

## Getting Started
This section will outline how to get up and running with this project.

### Prerequisites
Python version 2.6 or newer. Check this with `python -V`.
This program has been testing and works with `Python 3.5.2`, `Python 2.7.10`, and `Python 2.6.9`

### Installing
1. Clone project to local machine.
`git clone https://github.com/DrewWeth/Etsy_Proj`
2. Change directory to project
`cd Etsy_Proj`
3. Run main Python script.
`python source/main.py`

The main script is in the source folder to keep the root directory cleaner.

See usage section below view commands

## Usage
This section details how to use this project after successfully completing step 3 from the [installing](#installing) section

There are 3 main commands: add, list, and listen.
####ADD
The add command has 3 sub commands: artist, album, and track.
Before adding an album, the artist must exist.
Before adding a track, the album and artist must exist.
* USAGE: `add artist bob`
* USAGE: `add album The amazing race by bob`
* USAGE: `add track The amazing race`

####LIST
The list command has 3 subcommands and 1 optional value: artists, albums, tracks, and [top].
* USAGE: `list artists`
* USAGE: `list albums by bob`
* USAGE: `list tracks on Album Name by bob`
* USAGE: `list top q albums`
* USAGE: `list top 3 tracks`

####LISTEN
This command increments the play count on a track. You must provide the track, album, and artist.
* USAGE: `listen to song on album name by bob`

