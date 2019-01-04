import sys
import os

sys.path.append(os.path.expandvars('$ITV_PYTHON_CORE_MODULES'))
sys.path.append(os.path.expandvars('$ITV_PYTHON_MODULES'))
sys.path.append(os.path.expandvars('$PYTHON_MODULES'))

import itv_shell
import itv_argparser
import applications

### --- MAIN --- ###

parser = itv_argparser.parser(
os.path.dirname(__file__),
'''Opens Source Tree application from the path provided or
from the current working directory'''
)
parser.add_argument('-p','--path', help='Opens source tree from the given path')
args = parser.parse_args(sys.argv[1:])

if args.path:
    applications.open_sourcetree(path = args.path)
else:
    applications.open_sourcetree()
