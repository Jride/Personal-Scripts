import sys
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell
import itv_argparser
import itv_git

### --- MAIN --- ###

def update_repo():
    if not itv_git.is_git_repo():
        print("Not a git repo")
        sys.exit()

    itv_shell.run('git pull')

parser = itv_argparser.parser(
os.path.dirname(__file__),
'''
Updates the itv and josh scripts
'''
)
args = parser.parse_args(sys.argv[1:])

current_dir = itv_shell.result("pwd")

os.chdir(os.path.expandvars('$SCRIPTS'))
update_repo()

os.chdir(os.path.expandvars('$ITV_SCRIPTS'))
update_repo()

os.chdir(current_dir)
