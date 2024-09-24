import sys
import glob
import re
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))

import itv_shell

def setup_defaults():
    # Default to expanded save dialogue
    itv_shell.run("defaults write -g NSNavPanelExpandedStateForSaveMode -bool TRUE")

    # Prevent Photos from opening automatically when pluggin in devices
    itv_shell.run("defaults -currentHost write com.apple.ImageCapture disableHotPlug -bool true")

    # Text edit use plain text mode as default
    itv_shell.run("defaults write com.apple.TextEdit RichText -int 0")

    # Xcode display build times
    itv_shell.run("defaults write com.apple.dt.Xcode ShowBuildOperationDuration -bool YES")

    # Stop Textedit and other iCloud enabled apps from defaulting to save in iCloud
    itv_shell.run("defaults write NSGlobalDomain NSDocumentSaveNewDocumentsToCloud -bool false")


    # Set the default for the iOS Simulator to not use the hardware keyboard
    itv_shell.run("defaults write com.apple.iphonesimulator ConnectHardwareKeyboard 0")
    
    # Install sourcetree command line tools
    print("*** Copying sourcetree command line tools ***")
    itv_shell.run("cp /Applications/SourceTree.app/Contents/Resources/stree /usr/local/bin")

    # Install the sublime binary
    itv_shell.run(r"ln -s /Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl /usr/local/bin/subl")
