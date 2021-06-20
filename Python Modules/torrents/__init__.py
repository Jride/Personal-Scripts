import sys
import os
import re
import shutil

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell

scripts_path = os.path.expandvars('$SCRIPTS')
itv_scripts_path = os.path.expandvars('$ITV_SCRIPTS')

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
        if show in folders[key]:
            return key

    return None


def torrent_folders(torrent_media_folder):
    result = itv_shell.result("cd '%s' && ls -d */ | cut -f1 -d'/'" % torrent_media_folder)
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

def move_file(source, destination, dryrun):
    if os.path.isfile(destination):
        print("File exists... skipping >> " + destination)
        return False
    else:
        print("Move file to: " + destination)
        if dryrun is False:
            os.rename(source, destination)
            return True
        else:
            return False

def create_folder(folder, dryrun):
    if not os.path.exists(folder):
        print("Creating Folder: " + folder)
        if dryrun is False:
            os.makedirs(folder)