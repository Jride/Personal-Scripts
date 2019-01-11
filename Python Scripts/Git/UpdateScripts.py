import sys
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))
sys.path.append(os.path.expandvars('$PYTHON_MODULES'))

import itv_shell
import itv_argparser
import script_utils

### --- MAIN --- ###
parser = itv_argparser.parser(
os.path.dirname(__file__),
'''
Updates the itv and josh scripts
'''
)
args = parser.parse_args(sys.argv[1:])

script_utils.update_scripts()
