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

def clone_scripts_if_needed():
    
    if not os.path.exists(scripts_path) or not os.listdir(scripts_path):
        print("Personal Scripts Not Found")
        print("Checking our from repo...")
        itv_shell.run('git clone %s' % scripts_repo)

    if not os.path.exists(itv_scripts_path) or not os.listdir(itv_scripts_path):
        print("ITV Scripts Not Found")
        print("Checking our from repo...")
        itv_shell.run('git clone %s' % itv_scripts_repo)
