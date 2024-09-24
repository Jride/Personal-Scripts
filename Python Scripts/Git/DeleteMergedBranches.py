import sys
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))

import itv_shell
import itv_argparser

### --- MAIN --- ###

parser = itv_argparser.parser(
os.path.dirname(__file__),
'''
Deletes all local branches that have been merged into the current branch
'''
)
args = parser.parse_args(sys.argv[1:])

itv_shell.run(r'git branch --merged | egrep -v "(^\*|master|dev)" | xargs git branch -d')
