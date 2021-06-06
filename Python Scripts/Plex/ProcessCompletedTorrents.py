import sys
import os
from os.path import expanduser
import re
import glob
from pprint import pprint
import shutil

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))
sys.path.append(os.path.expandvars('$PYTHON_MODULES'))

import itv_shell
import itv_argparser
import notifications

### --- MAIN --- ###
parser = itv_argparser.parser(
    os.path.dirname(__file__),
    '''
    Checks for completed torrents, then renames and moves them into the correct plex media foldders
    '''
)
parser.add_argument('--dryrun', help='Run the script to show what actions will happen first', action="store_true")
parser.add_argument('--skipcleanup', help='Skips deleting the torrent folder', action="store_true")
args = parser.parse_args(sys.argv[1:])

home = expanduser("~")
TORRENT_TV_SHOWS = os.path.join(home, "torrents")
TORRENT_TV_SHOWS = os.path.join(TORRENT_TV_SHOWS, "tv_shows")

MEDIA_TV_SHOWS = os.path.join(home, "Videos")
MEDIA_TV_SHOWS = os.path.join(MEDIA_TV_SHOWS, "Media")
MEDIA_TV_SHOWS = os.path.join(MEDIA_TV_SHOWS, "TV Shows")

class Media:
    file_path = None
    file_name = None
    season_info = None
    extension = None

    def __init__(self, file_path, file_name, season_info):
        self.file_path = file_path
        self.file_name = file_name
        self.season_info = season_info
        self.extension = file_name[-4:]

    def print_desc(self):
        print("file_path: " + self.file_path)
        print("season_info: " + self.season_info)

class Torrent:
    identifier = None
    folder = None
    size = None
    done = None
    name = None
    media_list = []

    def __init__(self, identifier, folder, size, done):
        self.identifier = identifier
        self.folder = folder
        self.size = size
        self.done = done

    @property
    def is_done(self):
        return "100" in self.done

    def print_desc(self):
        print("ID: " + self.identifier)
        print("Folder: " + self.folder)
        print("DONE: " + self.done)

    def print_media_list(self):
        print("MEDIA LIST>>> %s" % len(self.media_list))
        for media in self.media_list:
            media.print_desc()

def result(command):
    return itv_shell.result("transmission-remote --auth transmission:transmission %s" % (command))

def remove_torrent(identifier):
    print("Removing torrent: " + identifier)
    if args.dryrun is False:
        itv_shell.run("transmission-remote --auth transmission:transmission -t %s --remove" % (identifier))

def delete_folder(folder):
    if os.path.isdir(folder) is False:
        print("Path is file not directory...skipping")
        return

    print("Deleting folder: " + folder)
    if args.dryrun is False and args.skipcleanup is False:
        shutil.rmtree(folder)

def existing_shows_folders():
    result = itv_shell.result("cd '%s' && ls -d */ | cut -f1 -d'/'" % MEDIA_TV_SHOWS)
    lines = result.splitlines()
    folders = {}
    for line in lines:
        folders[line] = [line]

        line_variation = line.lower()
        folders[line].append(line_variation)

        line_variation = line_variation.replace('(', '').replace(')', '')
        folders[line].append(line_variation)

        line_variation = line_variation.replace('-', '')
        folders[line].append(line_variation)

        line_variation = line_variation.replace('\'', '')
        folders[line].append(line_variation)

    return folders

def find_existing_folder_for_show(folders, show):
    for key in folders.keys():
        if show in folders[key]:
            return key

    return None


def torrent_folders():
    result = itv_shell.result("cd '%s' && ls -d */ | cut -f1 -d'/'" % TORRENT_TV_SHOWS)
    return result.splitlines()

def get_title(text):
    title_search = re.split("(s\d\de\d\d)", text)
    if title_search is not None:
        return title_search[0].replace('-', '').replace('.', ' ').replace('+', ' ').replace('!', '').strip()
    else:
        return None

def get_season_info(text):
    season_search = re.search("(s\d\de\d\d)", text)
    if season_search is not None:
        return season_search.group()
    else:
        return None

def move_file(source, destination):
    if os.path.isfile(destination):
        print("File exists... skipping >> " + destination)
        return False
    else:
        print("Move file to: " + destination)
        if args.dryrun is False:
            os.rename(source, destination)
            return True
        else:
            return False

def create_folder(folder):
    if not os.path.exists(folder):
        print("Creating Folder: " + folder)
        if args.dryrun is False:
            os.makedirs(folder)

existing_folders = existing_shows_folders()

completed_torrents = []
all_torrents = torrent_folders()
response = result("-l")
lines = response.splitlines()
# Removes header and footer from the printed table
del lines[0]
del lines[-1]

for index, line in enumerate(lines):
    text = line.strip()
    text = re.sub('(.) (.)', r'\1>>>space<<<\2', text)
    text = re.sub(' +', ' ', text)
    properties = text.split(' ')

    torrent = Torrent(
        properties[0].strip().replace('>>>space<<<', ' '),
        properties[-1].strip().replace('>>>space<<<', ' '),
        properties[2].strip().replace('>>>space<<<', ' '),
        properties[1].strip().replace('>>>space<<<', ' ')
    )

    # torrent.print_desc()

    folder = torrent.folder.lower()
    torrent.name = get_title(folder)

    # Only add the completed ones
    if torrent.is_done:
        completed_torrents.append(torrent)

    # Remove any processed torrent from the all torrents list
    if torrent.folder in all_torrents:
        all_torrents.remove(torrent.folder)

# Add any untracked completed torrents to the list
for torrent_folder in all_torrents:

    torrent = Torrent(
        None,
        torrent_folder,
        None,
        None
    )

    folder = torrent_folder.lower()
    torrent.name = get_title(folder)
    completed_torrents.append(torrent)

# Get all media files from torrents folder
types = ('*.avi', '*.mp4', '*.mkv', '*.flv', '*.mov', '*.wmv')
media_files = []
for files in types:
    search = os.path.join(TORRENT_TV_SHOWS, "**")
    search = os.path.join(search, files)
    media_files.extend(glob.glob(search, recursive=True))

# pprint(media_files)

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
            torrent_name = get_title(file_name.lower())
            if torrent_name is not None:
                torrent.name = torrent_name

            season_info = get_season_info(file_name.lower())
            if season_info is not None:
                media = Media(file_path, file_name, season_info)
                found_media.append(media)

    torrent.media_list = found_media
    # torrent.print_media_list()

# Process Completed Torrents Only
for torrent in completed_torrents:
    folder = find_existing_folder_for_show(existing_folders, torrent.name)

    if folder is None:
        new_folder = os.path.join(MEDIA_TV_SHOWS, torrent.name)
        create_folder(new_folder)
        existing_folders[torrent.name] = [torrent.name]
        folder = torrent.name

    if torrent.identifier is not None:
        remove_torrent(torrent.identifier)

    new_episode = False
    for media_file in torrent.media_list:
        destination = os.path.join(MEDIA_TV_SHOWS, folder)
        destination = os.path.join(destination, torrent.name.replace(" ", ".") + "." + media_file.season_info + media_file.extension)
        new_episode = move_file(media_file.file_path, destination)

    if new_episode:
        message = "New episode(s) available for " + torrent.name
        notifications.send("New Episode Available", message)

    torrent_folder = os.path.join(TORRENT_TV_SHOWS, torrent.folder)
    delete_folder(torrent_folder)
