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
Cleans up the .git folder by pruning and using "git rc"
'''
)
args = parser.parse_args(sys.argv[1:])

itv_shell.run('git remote prune origin')
itv_shell.run('git gc --prune=now')
