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
import script_utils

outdated_gems = []
new_updates = []

def update_brew_binary_if_needed(binary):
    if itv_shell.result("brew outdated " + binary):
        results = itv_shell.result("brew upgrade " + binary)
        updates = '''
---- Start Updating %s -----

%s

---- Finished Updating %s -----

    ''' % (binary, results, binary)
        new_updates.append(updates)

def update_gem_dependency_if_needed(gem_to_update):
    for outdated_gem in outdated_gems:
        if outdated_gem == gem_to_update:
            results = itv_shell.result("gem update " + gem_to_update)
            updates = '''
---- Start Updating Gem: %s -----

%s

---- Finished Updating Gem: %s -----

    ''' % (gem_to_update, results, gem_to_update)
            new_updates.append(updates)

### --- MAIN --- ###

# Setup the Mac Defaults
mac_utils.setup_defaults()

# Update Podspec ENV variables
cocoapods.generate_pod_aliases()

# Clone / Update the scripts
script_utils.update_scripts()

# Update Homebrew
itv_shell.run("brew update")

# Homebrew updates

update_brew_binary_if_needed("rbenv")
update_brew_binary_if_needed("swiftlint")
update_brew_binary_if_needed("carthage")
update_brew_binary_if_needed("git")
update_brew_binary_if_needed("git-lfs")

# Update Gem Libraries
outdated_gems_result = itv_shell.result("gem outdated")
outdated_gems_list = outdated_gems_result.splitlines()
for gem in outdated_gems_list:
    split_gem = gem.split(" ")
    outdated_gems.append(split_gem[0])

update_gem_dependency_if_needed("fastlane")
update_gem_dependency_if_needed("cocoapods")
update_gem_dependency_if_needed("cocoapods-rome")

itv_shell.run("pod repo update")

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
