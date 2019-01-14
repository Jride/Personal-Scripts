import sys
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell
import itv_logger
import itv_git

scripts_path = os.path.expandvars('$SCRIPTS')
itv_scripts_path = os.path.expandvars('$ITV_SCRIPTS')

scripts_repo = 'https://github.com/Jride/Personal-Scripts.git'
itv_scripts_repo = 'https://github.com/ITV/iOS-Team-Scripts.git'

def update_scripts():
    def update_repo():
        if not itv_git.is_git_repo():
            print("Not a git repo")
            sys.exit()

        itv_shell.run('git pull')

    current_dir = itv_shell.result("pwd")

    os.chdir(scripts_path)
    update_repo()

    os.chdir(itv_scripts_path)
    update_repo()

    os.chdir(current_dir)
