import sys
import os

home_dir = os.path.expanduser('~') + "/"
# Getting access to our py utilities folder
common_py_path = home_dir + "Dropbox/Mac_Utilities/Scripts/py_utilities"
sys.path.insert(0, common_py_path)

from utility_terminal import shell_command

def setup_mac_defaults():
    # Default to expanded save dialogue
    shell_command("defaults write -g NSNavPanelExpandedStateForSaveMode -bool TRUE")

    # Prevent Photos from opening automatically when pluggin in devices
    shell_command("defaults -currentHost write com.apple.ImageCapture disableHotPlug -bool true")

    # Text edit use plain text mode as default
    shell_command("defaults write com.apple.TextEdit RichText -int 0")

    # Xcode display build times
    shell_command("defaults write com.apple.dt.Xcode ShowBuildOperationDuration -bool YES")

    # Stop Textedit and other iCloud enabled apps from defaulting to save in iCloud
    shell_command("defaults write NSGlobalDomain NSDocumentSaveNewDocumentsToCloud -bool false")

    # Install sourcetree command line tools
    print("*** Copying sourcetree command line tools ***")
    shell_command("cp /Applications/SourceTree.app/Contents/Resources/stree /usr/local/bin")

    # Set the default for the iOS Simulator to not use the hardware keyboard
    shell_command("defaults write com.apple.iphonesimulator ConnectHardwareKeyboard 0")
