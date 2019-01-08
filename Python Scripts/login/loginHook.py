import sys
import os
import socket
import datetime

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))
sys.path.append(os.path.expandvars('$PYTHON_MODULES'))

import itv_shell
import itv_argparser
import itv_filesystem
import cocoapods
import mac_utils

computer_name = socket.gethostname()
new_updates = []

def update_binary_if_needed(binary):
    if itv_shell.result("brew outdated " + binary):
        results = itv_shell.result("brew upgrade " + binary)
        updates = '''
---- Start Updating %s -----

%s

---- Finished Updating %s -----

    ''' % (binary, results, binary)
        new_updates.append(updates)

### --- MAIN --- ###

args = sys.argv[1:]

# Parse the arguments
parser = itv_argparser.parser(
os.path.dirname(__file__),
'Runs the daily login hook to update the brew packages amongst other things'
)
args = parser.parse_args(args)

# Setup the Mac Defaults
mac_utils.setup_defaults()

itv_shell.run("pod repo update")

# Update Podspec ENV variables
cocoapods.generate_pod_aliases()

# Update Homebrew
itv_shell.run("brew update")

# cocoapod updates
update_binary_if_needed("cocoapods")

# swiftlint updates
update_binary_if_needed("swiftlint")

# git updates
update_binary_if_needed("git")

# marathon for editing swift scripts
update_binary_if_needed("")

# If any new updates store the output to disk and send via email
if new_updates:
    now = datetime.datetime.now().strftime("%A %d %B %Y %H:%M")
    update_on = "\nUPDATED ON %s\n" % (now)
    new_updates.insert(0, update_on)
    new_updates_txt = ''.join(new_updates)
    # Store the updates via txt file
    file_path = os.path.expandvars('$BREW_PACKAGE_UPDATES')
    itv_filesystem.write_text_to_file(new_updates_txt, file_path, "w+")

    icon = "https://brew.sh/assets/img/homebrew-256x256.png"
    title = "'Packages Updated!'"
    message = "'Click here to see what has packages have been updated'"
    action = "'open -a TextEdit %s'" % file_path

    itv_shell.run("terminal-notifier -group 'homebrew-updates'"
    + " -title " + title
    + " -message " + message
    + " -sound Glass"
    + " -execute " + action
    + " -appIcon " + icon)
