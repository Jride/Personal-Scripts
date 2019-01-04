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
'''Opens the provided file in the TextEdit application'''
)
parser.add_argument('file', help='Path to the file to open')
args = parser.parse_args(sys.argv[1:])

applications.open_textedit(file = args.file)
