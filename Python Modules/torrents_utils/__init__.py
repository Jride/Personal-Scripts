import sys
import os
import re
import shutil
from difflib import SequenceMatcher

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell

scripts_path = os.path.expandvars('$SCRIPTS')
itv_scripts_path = os.path.expandvars('$ITV_SCRIPTS')

class Media:
    file_path = None
    file_name = None
    season_info = None
    extension = None

    def __init__(self, file_path, file_name, season_info=None):
        self.file_path = file_path
        self.file_name = file_name
        self.season_info = season_info
        self.extension = file_name[-4:]

    def print_desc(self):
        print("file_path: " + self.file_path)
        if self.season_info is not None:
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

    def media(self, media_type):
        if media_type == "movie":
            ratio = 0
            media_item = None

            for item in self.media_list:
                new_ratio = similar(item.file_name, self.folder)
                print("Comparing: " + item.file_name + " with: " + self.folder)
                print(new_ratio)
                if new_ratio > ratio:
                    ratio = new_ratio
                    media_item = item

            return [media_item]
        else:
            return self.media_list

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def result(command):
    return itv_shell.result("transmission-remote --auth transmission:transmission %s" % (command))

def remove_torrent(identifier, dryrun):
    print("Removing torrent: " + identifier)
    if dryrun is False:
        itv_shell.run("transmission-remote --auth transmission:transmission -t %s --remove" % (identifier))

def delete_folder(folder, dryrun, skipcleanup):
    if os.path.isdir(folder) is False:
        print("Path is file not directory...skipping")
        return

    print("Deleting folder: " + folder)
    if dryrun is False and skipcleanup is False:
        shutil.rmtree(folder)

def existing_shows_folders(media_folder):
    result = itv_shell.result("cd '%s' && ls -d */ | cut -f1 -d'/'" % media_folder)
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
        if "eastenders" in show:
            if "eastenders" in folders[key]:
                return key
        else:
            if show in folders[key]:
                return key

    return None


def torrent_folders(torrent_media_folder):
    result = itv_shell.result("cd '%s' && ls -d */ | cut -f1 -d'/'" % torrent_media_folder)
    return result.splitlines()

def get_title(text):
    text = text.replace('-', '').replace('.', ' ').replace('+', ' ').replace('!', '').strip()
    return text

def contains_episodic_info(text):
    result = re.search("[-. ]?s[0-9]+e[0-9]+", text.lower())

    if result:
      return True
    else:
      return False

def is_long_running_show(text):
    shows = ["eastenders"]
    return any(show in text.lower() for show in shows)


def get_season_info(text):

    season_search = re.search(r"(s\d\de\d\d)", text)
    if season_search is not None:
        return season_search.group()
    else:
        return None

def move_file(source, destination, dryrun):
    if os.path.isfile(destination):
        print("File exists... skipping >> " + destination)
        return False
    else:
        print("Move file to: " + destination)
        if dryrun is False:
            shutil.move(source, destination)
            return True
        else:
            return False

def create_folder(folder, dryrun):
    if not os.path.exists(folder):
        print("Creating Folder: " + folder)
        if dryrun is False:
            os.makedirs(folder)
