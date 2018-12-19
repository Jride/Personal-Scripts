import sys
import os
import socket
import datetime

home_dir = os.path.expanduser('~') + "/"
# Getting access to our py utilities folder
common_py_path = home_dir + "Dropbox/Mac_Utilities/Scripts/py_utilities"
sys.path.insert(0, common_py_path)

from setupMacDefaults import setup_mac_defaults
from utility_email import send_email
from utility_terminal import shell_result
from utility_terminal import shell_command
from utility_filemanager import write_text_to_file
from utility_filemanager import open_text_file

computer_name = socket.gethostname()
generatePodAliases = home_dir + "Dropbox/Mac_Utilities/Swift\ Scripts/GeneratePodAliases.swift"

swift = '/usr/bin/swift'

new_updates = []

def update_binary_if_needed(binary):
    if shell_result("brew outdated " + binary):
        results = shell_result("brew upgrade " + binary)
        updates = '''
---- Start Updating %s -----

%s

---- Finished Updating %s -----

    ''' % (binary, results, binary)
        new_updates.append(updates)

# MAIN SCRIPT

# Setup the Mac Defaults
setup_mac_defaults()

shell_command("pod repo update")

# Update Podspec ENV variables
shell_command(swift + " " + generatePodAliases)

# Update Homebrew
shell_command("brew update")

# cocoapod updates
update_binary_if_needed("cocoapods")

# swiftlint updates
update_binary_if_needed("swiftlint")

# git updates
update_binary_if_needed("git")

# If any new updates store the output to disk and send via email
if new_updates:
    now = datetime.datetime.now().strftime("%A %d %B %Y %H:%M")
    update_on = "\nUPDATED ON %s\n" % (now)
    new_updates.insert(0, update_on)
    new_updates_txt = ''.join(new_updates)
    # Store the updates via txt file
    file_path = home_dir + "Documents/.packageUpdates/updates.txt"
    write_text_to_file(new_updates_txt, file_path, "w+")

    icon = "https://brew.sh/assets/img/homebrew-256x256.png"
    title = "'Packages Updated!'"
    message = "'Click here to see what has packages have been updated'"
    action = home_dir + "Dropbox/Mac_Utilities/Scripts/login/OpenUpdateFile.sh"

    shell_command("terminal-notifier -group 'homebrew-updates'"
    + " -title " + title
    + " -message " + message
    + " -sound Glass"
    + " -execute " + action
    + " -appIcon " + icon)
