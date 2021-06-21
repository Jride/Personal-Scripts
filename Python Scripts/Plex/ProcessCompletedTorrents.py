import sys
import os
from os.path import expanduser
import re
import glob
from pprint import pprint

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))
sys.path.append(os.path.expandvars('$PYTHON_MODULES'))

import itv_argparser
import notifications
import torrents

### --- MAIN --- ###
parser = itv_argparser.parser(
    os.path.dirname(__file__),
    '''
    Checks for completed torrents, then renames and moves them into the correct plex media foldders
    '''
)
parser.add_argument('-mediaType', help='show, movie, kids_show, kids_movie')
parser.add_argument('--dryrun', help='Run the script to show what actions will happen first', action="store_true")
parser.add_argument('--skipcleanup', help='Skips deleting the torrent folder', action="store_true")
args = parser.parse_args(sys.argv[1:])

home = expanduser("~")
TORRENT_MEDIA_FOLDER = os.path.join(home, "torrents")
torrentFolderName = "tv_shows"

if args.mediaType == "movie":
    torrentFolderName = "movies"

if args.mediaType == "kids_show":
    torrentFolderName = "kids_shows"

if args.mediaType == "kids_movie":
    torrentFolderName = "kids_movies"

TORRENT_MEDIA_FOLDER = os.path.join(TORRENT_MEDIA_FOLDER, torrentFolderName)

MEDIA_FOLDER = os.path.join(home, "Videos")
MEDIA_FOLDER = os.path.join(MEDIA_FOLDER, "Media")
# "TV Shows"

mediaFolderName = "TV Shows"

if args.mediaType == "movie":
    mediaFolderName = "Movies"

if args.mediaType == "kids_show":
    mediaFolderName = "Kids/TV Shows"

if args.mediaType == "kids_movie":
    mediaFolderName = "Kids/Movies"

MEDIA_FOLDER = os.path.join(MEDIA_FOLDER, mediaFolderName)

IS_MOVIE = False
if args.mediaType == "movie" or args.mediaType == "kids_movie":
    IS_MOVIE = True

completed_torrents = []
all_torrents = torrents.torrent_folders(TORRENT_MEDIA_FOLDER)
response = torrents.result("-l")
lines = response.splitlines()

if args.verbose:
    print(all_torrents)

# Removes header and footer from the printed table
del lines[0]
del lines[-1]

for index, line in enumerate(lines):
    text = line.strip()
    text = re.sub('(.) (.)', r'\1>>>space<<<\2', text)
    text = re.sub(' +', ' ', text)
    properties = text.split(' ')

    torrent = torrents.Torrent(
        properties[0].strip().replace('>>>space<<<', ' '),
        properties[-1].strip().replace('>>>space<<<', ' '),
        properties[2].strip().replace('>>>space<<<', ' '),
        properties[1].strip().replace('>>>space<<<', ' ')
    )

    if args.verbose:
        torrent.print_desc()

    folder = torrent.folder.lower()
    torrent.name = torrents.get_title(folder, IS_MOVIE)

    # Only add the completed ones
    if torrent.is_done:
        completed_torrents.append(torrent)

    # Remove any processed torrent from the all torrents list
    if torrent.folder in all_torrents:
        all_torrents.remove(torrent.folder)

# Add any untracked completed torrents to the list
for torrent_folder in all_torrents:

    torrent = torrents.Torrent(
        None,
        torrent_folder,
        None,
        None
    )

    folder = torrent_folder.lower()
    torrent.name = torrents.get_title(folder, IS_MOVIE)
    completed_torrents.append(torrent)

# Get all media files from torrents folder
types = ('*.avi', '*.mp4', '*.mkv', '*.flv', '*.mov', '*.wmv')
media_files = []
for files in types:
    search = os.path.join(TORRENT_MEDIA_FOLDER, "**")
    search = os.path.join(search, files)
    media_files.extend(glob.glob(search, recursive=True))

if args.verbose:
    pprint(media_files)

# Build up media files info
for torrent in completed_torrents:
    found_media = []
    for file_path in media_files:
        if torrent.folder in file_path:
            # print(file_path)
            # print(torrent_folder)
            file_name_chunks = file_path.split("/")
            file_name = file_name_chunks[-1]

            # print(file_name)
            torrent_name = torrents.get_title(file_name.lower(), IS_MOVIE)
            if torrent_name is not None:
                torrent.name = torrent_name

            if IS_MOVIE:
                media = torrents.Media(file_path, file_name)
                found_media.append(media)
            else:
                season_info = torrents.get_season_info(file_name.lower())
                if season_info is not None:
                    media = torrents.Media(file_path, file_name, season_info)
                    found_media.append(media)

    torrent.media_list = found_media

    if args.verbose:
        torrent.print_media_list()

# Process Completed Torrents Only
for torrent in completed_torrents:

    if IS_MOVIE is False:
        existing_folders = torrents.existing_shows_folders(MEDIA_FOLDER)
        folder = torrents.find_existing_folder_for_show(existing_folders, torrent.name)
        if folder is None:
            new_folder = os.path.join(MEDIA_FOLDER, torrent.name)
            torrents.create_folder(new_folder, args.dryrun)
            existing_folders[torrent.name] = [torrent.name]
            folder = torrent.name

    if torrent.identifier is not None:
        torrents.remove_torrent(torrent.identifier, args.dryrun)

    new_media = False
    for media_file in torrent.media(args.mediaType):

        if IS_MOVIE:
            destination = os.path.join(MEDIA_FOLDER, media_file.file_name)
        else:
            destination = os.path.join(MEDIA_FOLDER, folder)
            destination = os.path.join(destination, torrent.name.replace(" ", ".") + "." + media_file.season_info + media_file.extension)

        new_media = torrents.move_file(media_file.file_path, destination, args.dryrun)

    if new_media:
        if IS_MOVIE:
            message = "Movie finished downloading: " + torrent.name
            notifications.send("Movie Download Complete", message)
        else:
            message = "New episode(s) available for " + torrent.name
            notifications.send("New Episode Available", message)

    torrent_folder = os.path.join(TORRENT_MEDIA_FOLDER, torrent.folder)
    torrents.delete_folder(torrent_folder, args.dryrun, args.skipcleanup)
